from django.urls import include, path

from .apps import GoldenViewWellnessApiConfig as AppConfig
from .routers import router

API_VERSION_PREFIX = "v1"

app_name = AppConfig.name

urlpatterns = [
    path(f"{API_VERSION_PREFIX}/", include(router.urls)),
]
