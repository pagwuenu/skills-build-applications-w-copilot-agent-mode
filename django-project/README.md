# OctoFit Django project

This is a standalone Django project scaffold. Its dependencies are listed in the
workspace-root `requirements.txt`; the existing OctoFit React/Express/MongoDB
application is unchanged.

From the workspace root, install dependencies and check the project:

```sh
python -m pip install -r requirements.txt
python django-project/manage.py check
```

To run it locally, use port `8001` so it does not conflict with the existing
Express API on port `8000`:

```sh
python django-project/manage.py runserver 127.0.0.1:8001
```

The starter deliberately omits Django's admin, authentication, and session
components.
