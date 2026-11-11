from django.urls import path

from . import views


urlpatterns = [
    path("users/", views.users, name="users"),
    path("teams/", views.teams, name="teams"),
    path("activities/", views.activities, name="activities"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("workouts/", views.workouts, name="workouts"),
    path(
        "workouts/suggestions/<str:user_email>/",
        views.workout_suggestions,
        name="workout_suggestions",
    ),
]
