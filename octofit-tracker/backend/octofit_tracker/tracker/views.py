import json
from datetime import datetime, timezone

from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods

from .models import get_collection
from .serializers import serialize_document, serialize_documents


def api_root(_request):
    return JsonResponse(
        {
            "users": "/api/users/",
            "teams": "/api/teams/",
            "activities": "/api/activities/",
            "leaderboard": "/api/leaderboard/",
            "workouts": "/api/workouts/",
            "workoutSuggestions": "/api/workouts/suggestions/<userEmail>/",
        }
    )


def _json_body(request):
    try:
        value = json.loads(request.body)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _bad_request(message):
    return JsonResponse({"error": message}, status=400)


@require_GET
def users(request):
    del request
    return JsonResponse({"users": serialize_documents(get_collection("users").find())})


@require_http_methods(["GET", "POST"])
def teams(request):
    collection = get_collection("teams")
    if request.method == "GET":
        return JsonResponse({"teams": serialize_documents(collection.find())})

    body = _json_body(request)
    if body is None:
        return _bad_request("Request body must be a JSON object")
    name = body.get("name")
    mascot = body.get("mascot")
    if not isinstance(name, str) or not name.strip():
        return _bad_request("A team name is required")
    if not isinstance(mascot, str) or not mascot.strip():
        return _bad_request("A team mascot is required")

    member_ids = body.get("members", [])
    if not isinstance(member_ids, list) or any(
        not isinstance(member_id, str) or not ObjectId.is_valid(member_id)
        for member_id in member_ids
    ):
        return _bad_request("Members must be an array of valid user IDs")

    members = [ObjectId(member_id) for member_id in member_ids]
    user_collection = get_collection("users")
    if any(user_collection.find_one({"_id": member_id}) is None for member_id in members):
        return _bad_request("Every team member must reference an existing user")

    team = {"name": name.strip(), "mascot": mascot.strip(), "members": members}
    team["_id"] = collection.insert_one(team).inserted_id
    return JsonResponse({"team": serialize_document(team)}, status=201)


@require_http_methods(["GET", "POST"])
def activities(request):
    collection = get_collection("activities")
    if request.method == "GET":
        return JsonResponse({"activities": serialize_documents(collection.find())})

    body = _json_body(request)
    if body is None:
        return _bad_request("Request body must be a JSON object")

    user_id = body.get("userId")
    team_id = body.get("teamId")
    activity_type = body.get("type")
    minutes = body.get("minutes")
    if not isinstance(user_id, str) or not ObjectId.is_valid(user_id):
        return _bad_request("A valid userId is required")
    if not isinstance(team_id, str) or not ObjectId.is_valid(team_id):
        return _bad_request("A valid teamId is required")
    if not isinstance(activity_type, str) or not activity_type.strip():
        return _bad_request("An activity type is required")
    if isinstance(minutes, bool) or not isinstance(minutes, int) or minutes <= 0:
        return _bad_request("Minutes must be a positive integer")

    user_id = ObjectId(user_id)
    team_id = ObjectId(team_id)
    if get_collection("users").find_one({"_id": user_id}) is None:
        return JsonResponse({"error": "User not found"}, status=404)
    if get_collection("teams").find_one({"_id": team_id}) is None:
        return JsonResponse({"error": "Team not found"}, status=404)

    activity = {
        "user": user_id,
        "team": team_id,
        "type": activity_type.strip(),
        "minutes": minutes,
        "points": minutes,
        "occurredAt": datetime.now(timezone.utc),
    }
    activity["_id"] = collection.insert_one(activity).inserted_id
    return JsonResponse({"activity": serialize_document(activity)}, status=201)


@require_GET
def leaderboard(request):
    del request
    totals = {}
    for activity in get_collection("activities").find():
        team_id = activity.get("team")
        if team_id is not None:
            totals[team_id] = totals.get(team_id, 0) + activity.get("points", 0)

    teams_by_id = {
        team["_id"]: team for team in get_collection("teams").find()
    }
    ranked = sorted(
        (
            (teams_by_id[team_id].get("name", ""), points)
            for team_id, points in totals.items()
            if team_id in teams_by_id
        ),
        key=lambda item: (-item[1], item[0]),
    )
    return JsonResponse(
        {
            "leaderboard": [
                {"teamName": team_name, "totalPoints": points, "rank": rank}
                for rank, (team_name, points) in enumerate(ranked, start=1)
            ]
        }
    )


@require_GET
def workouts(request):
    del request
    return JsonResponse({"workouts": serialize_documents(get_collection("workouts").find())})


@require_GET
def workout_suggestions(request, user_email):
    del request
    user = get_collection("users").find_one({"email": user_email})
    if user is None:
        return JsonResponse({"error": "User not found"}, status=404)

    activities_collection = get_collection("activities")
    recent_activity = activities_collection.find_one(
        {"user": user["_id"]}, sort=[("occurredAt", -1)]
    )
    activity_focus = None
    if recent_activity:
        activity_focus = {
            "run": "endurance",
            "walk": "endurance",
            "cycle": "endurance",
            "strength": "strength",
        }.get(recent_activity.get("type"), recent_activity.get("type"))

    workout_documents = list(get_collection("workouts").find())
    available_focuses = {workout.get("focus") for workout in workout_documents}
    goal = user.get("fitnessGoal")
    if goal in available_focuses:
        preferred_focus = goal
        preference_reason = "fitness goal"
    elif activity_focus in available_focuses:
        preferred_focus = activity_focus
        preference_reason = "recent activity"
    else:
        preferred_focus = goal or activity_focus
        preference_reason = "fitness goal" if goal else "recent activity"

    matching = [
        workout for workout in workout_documents
        if preferred_focus and workout.get("focus") == preferred_focus
    ]
    alternatives = [workout for workout in workout_documents if workout not in matching]
    ordered = matching + alternatives
    suggestions = []
    for workout in ordered:
        suggestion = serialize_document(workout)
        if workout in matching:
            reason = f"Matches the user's {preferred_focus} {preference_reason}."
        elif activity_focus and workout.get("focus") == activity_focus:
            reason = f"Matches the user's recent {recent_activity.get('type')} activity."
        else:
            reason = "Recommended as an alternative workout."
        suggestion["reason"] = reason
        suggestions.append(suggestion)
    return JsonResponse({"suggestions": suggestions})
