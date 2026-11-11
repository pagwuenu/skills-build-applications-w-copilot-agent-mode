import json
from datetime import datetime, timezone
from unittest.mock import patch

from bson import ObjectId
from django.test import SimpleTestCase


class FakeCollection:
    def __init__(self, documents=()):
        self.documents = list(documents)

    def find(self, query=None):
        return [
            document for document in self.documents
            if all(document.get(key) == value for key, value in (query or {}).items())
        ]

    def find_one(self, query=None, sort=None):
        matches = self.find(query)
        if sort and matches:
            field, direction = sort[0]
            matches.sort(key=lambda document: document.get(field), reverse=direction < 0)
        return matches[0] if matches else None

    def insert_one(self, document):
        document["_id"] = ObjectId()
        self.documents.append(document)
        return type("InsertResult", (), {"inserted_id": document["_id"]})()


class OctoFitApiTests(SimpleTestCase):
    def setUp(self):
        self.user_id = ObjectId()
        self.team_id = ObjectId()
        self.user_documents = FakeCollection(
            [{"_id": self.user_id, "name": "Mona", "email": "mona@example.com", "fitnessGoal": "endurance"}]
        )
        self.team_documents = FakeCollection(
            [{"_id": self.team_id, "name": "Octocats", "mascot": "Mona", "members": [self.user_id]}]
        )
        self.activity_documents = FakeCollection(
            [{
                "_id": ObjectId(),
                "user": self.user_id,
                "team": self.team_id,
                "type": "run",
                "minutes": 25,
                "points": 25,
                "occurredAt": datetime(2026, 1, 10, tzinfo=timezone.utc),
            }]
        )
        self.workout_documents = FakeCollection(
            [
                {"_id": ObjectId(), "title": "Intervals", "focus": "endurance", "minutes": 30, "difficulty": "moderate"},
                {"_id": ObjectId(), "title": "Strength Circuit", "focus": "strength", "minutes": 30, "difficulty": "moderate"},
            ]
        )
        self.collections = {
            "users": self.user_documents,
            "teams": self.team_documents,
            "activities": self.activity_documents,
            "workouts": self.workout_documents,
        }
        self.collection_patcher = patch(
            "tracker.views.get_collection",
            side_effect=lambda name: self.collections[name],
        )
        self.collection_patcher.start()
        self.addCleanup(self.collection_patcher.stop)

    def test_api_root_points_to_api(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["teams"], "/api/teams/")
        self.assertEqual(response.json()["workoutSuggestions"], "/api/workouts/suggestions/<userEmail>/")

    def test_lists_users_and_workouts(self):
        users_response = self.client.get("/api/users/")
        workouts_response = self.client.get("/api/workouts/")
        self.assertEqual(users_response.status_code, 200)
        self.assertEqual(users_response.json()["users"][0]["email"], "mona@example.com")
        self.assertEqual(workouts_response.status_code, 200)
        self.assertEqual(len(workouts_response.json()["workouts"]), 2)

    def test_api_allows_configured_vite_origin(self):
        response = self.client.options(
            "/api/teams/",
            HTTP_ORIGIN="http://localhost:5173",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="GET",
        )
        self.assertEqual(response["Access-Control-Allow-Origin"], "http://localhost:5173")

    def test_lists_collection_documents_and_serializes_ids(self):
        response = self.client.get("/api/teams/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["teams"][0]["id"], str(self.team_id))
        self.assertEqual(response.json()["teams"][0]["members"], [str(self.user_id)])

    def test_creates_team_and_rejects_missing_name(self):
        invalid = self.client.post("/api/teams/", data=json.dumps({"mascot": "Mona"}), content_type="application/json")
        self.assertEqual(invalid.status_code, 400)

        created = self.client.post(
            "/api/teams/",
            data=json.dumps({"name": "RoboCats", "mascot": "Hubot", "members": [str(self.user_id)]}),
            content_type="application/json",
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["team"]["name"], "RoboCats")

    def test_creates_activity_and_rejects_malformed_reference(self):
        invalid = self.client.post(
            "/api/activities/",
            data=json.dumps({"userId": "invalid", "teamId": str(self.team_id), "type": "run", "minutes": 10}),
            content_type="application/json",
        )
        self.assertEqual(invalid.status_code, 400)

        created = self.client.post(
            "/api/activities/",
            data=json.dumps({"userId": str(self.user_id), "teamId": str(self.team_id), "type": "run", "minutes": 10}),
            content_type="application/json",
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["activity"]["points"], 10)

    def test_leaderboard_orders_teams_by_points(self):
        second_team_id = ObjectId()
        self.team_documents.documents.append(
            {"_id": second_team_id, "name": "Robocats", "mascot": "Hubot", "members": []}
        )
        self.activity_documents.documents.append(
            {"_id": ObjectId(), "team": second_team_id, "points": 35}
        )

        response = self.client.get("/api/leaderboard/")
        self.assertEqual(
            response.json()["leaderboard"],
            [
                {"teamName": "Robocats", "totalPoints": 35, "rank": 1},
                {"teamName": "Octocats", "totalPoints": 25, "rank": 2},
            ],
        )

    def test_workout_suggestions_match_goal_and_unknown_users_return_404(self):
        response = self.client.get("/api/workouts/suggestions/mona%40example.com/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["suggestions"][0]["focus"], "endurance")
        self.assertIn("goal", response.json()["suggestions"][0]["reason"])

        self.user_documents.documents[0]["fitnessGoal"] = "mobility"
        activity_match = self.client.get("/api/workouts/suggestions/mona%40example.com/")
        self.assertEqual(activity_match.json()["suggestions"][0]["focus"], "endurance")
        self.assertIn("recent activity", activity_match.json()["suggestions"][0]["reason"])

        self.assertEqual(
            self.client.get("/api/workouts/suggestions/unknown%40example.com/").status_code,
            404,
        )
