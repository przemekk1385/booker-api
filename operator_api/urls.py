from django.urls import include, path

from operator_api.apps import OperatorApiConfig as AppConfig
from operator_api.routers import router

API_VERSION_PREFIX = "v1"

app_name = AppConfig.name

urlpatterns = [
    path(f"{API_VERSION_PREFIX}/", include(router.urls)),
]
