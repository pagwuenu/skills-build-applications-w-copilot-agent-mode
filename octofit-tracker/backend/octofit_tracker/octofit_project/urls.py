from django.urls import include, path

from tracker.views import api_root


urlpatterns = [
    path("", api_root, name="api_root"),
    path("api/", include("tracker.urls")),
]
