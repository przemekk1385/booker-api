from django.urls import include, path

from booker_api.apps import BookerApiConfig as AppConfig
from booker_api.routers import router

API_VERSION_PREFIX = "v1"

app_name = AppConfig.name

urlpatterns = [
    path(f"{API_VERSION_PREFIX}/", include(router.urls)),
]
