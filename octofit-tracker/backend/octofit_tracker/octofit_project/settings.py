import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "octofit-django-development-key")
DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
ALLOWED_HOSTS.extend(
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
)
codespace_name = os.getenv("CODESPACE_NAME")
if codespace_name:
    ALLOWED_HOSTS.extend([codespace_name, f"{codespace_name}-8000.app.github.dev"])
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.staticfiles",
    "tracker.apps.TrackerConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "octofit_project.urls"
WSGI_APPLICATION = "octofit_project.wsgi.application"
ASGI_APPLICATION = "octofit_project.asgi.application"

TEMPLATES = []

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/octofit_db")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "octofit_db")

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]
CORS_URLS_REGEX = r"^/api/.*$"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
