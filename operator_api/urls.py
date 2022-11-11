from django.urls import include, path, re_path

from operator_api import views
from operator_api.apps import OperatorApiConfig as AppConfig
from operator_api.routers import router

API_VERSION_PREFIX = "v1"

app_name = AppConfig.name

urlpatterns = [
    path(f"{API_VERSION_PREFIX}/", include(router.urls)),
    re_path(rf"^{API_VERSION_PREFIX}/health/$", views.health, name="health"),
]
