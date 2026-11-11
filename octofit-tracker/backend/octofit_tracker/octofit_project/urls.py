import os

from django.http import JsonResponse
from django.urls import include, path

from tracker.views import api_root


def codespace_api_root(request):
    codespace_name = os.getenv("CODESPACE_NAME")
    codespace_host = f"{codespace_name}-8000.app.github.dev" if codespace_name else None
    if request.get_host() != codespace_host:
        return api_root(request)

    base_url = f"https://{codespace_host}"
    return JsonResponse(
        {
            "users": f"{base_url}/api/users/",
            "teams": f"{base_url}/api/teams/",
            "activities": f"{base_url}/api/activities/",
            "leaderboard": f"{base_url}/api/leaderboard/",
            "workouts": f"{base_url}/api/workouts/",
            "workoutSuggestions": f"{base_url}/api/workouts/suggestions/<userEmail>/",
        }
    )


urlpatterns = [
    path("", codespace_api_root, name="api_root"),
    path("api/", include("tracker.urls")),
]
