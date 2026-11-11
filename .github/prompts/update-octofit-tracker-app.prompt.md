---
description: "Update the OctoFit Tracker Django backend and API"
agent: 'agent'
mode: 'agent'
model: GPT-4.1
---

# Django App Updates

Update the Django project in `octofit-tracker/backend/octofit_tracker`.

1. Update `settings.py` for the MongoDB connection and CORS.
2. Update `models.py`, `serializers.py`, `urls.py`, `views.py`, `tests.py`, and `admin.py` to support the users, teams, activities, leaderboard, and workouts collections.
3. Ensure `/` points to the API and `api_root` is present in `urls.py`.

Follow the existing project conventions, add or update tests for the behavior, and run the relevant checks.
