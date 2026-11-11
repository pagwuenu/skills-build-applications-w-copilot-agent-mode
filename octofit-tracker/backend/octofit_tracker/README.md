# OctoFit Django API

This Django API is a separate backend service alongside the existing Express API.
It reads and writes the same MongoDB database and collections, defaults to
`octofit_db` on `localhost:27017`, and does not replace Express on port `8000`.

Install the workspace Python dependencies and start Django on a separate port:

```sh
python -m pip install -r requirements.txt
python octofit-tracker/backend/octofit_tracker/manage.py check
python octofit-tracker/backend/octofit_tracker/manage.py test tracker.tests
python octofit-tracker/backend/octofit_tracker/manage.py runserver 127.0.0.1:8001
```

Set `MONGODB_URI` and `MONGODB_DATABASE` to override the MongoDB connection.
Set `CORS_ALLOWED_ORIGINS` to a comma-separated list of trusted browser origins.
The default allows the local Vite origin on port `5173`.

The JSON API root is `/`; collection endpoints are under `/api/`.
