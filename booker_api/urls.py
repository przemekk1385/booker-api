from django.urls import include, path, re_path

from booker_api import views
from booker_api.apps import BookerApiConfig as AppConfig
from booker_api.routers import router

API_VERSION_PREFIX = "v1"

app_name = AppConfig.name

urlpatterns = [
    path(f"{API_VERSION_PREFIX}/", include(router.urls)),
    re_path(rf"^{API_VERSION_PREFIX}/slot/$", views.slot_list, name="slot-list"),
    re_path(rf"^{API_VERSION_PREFIX}/health/$", views.health, name="health"),
]
