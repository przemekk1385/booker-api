from django.urls import include, path, re_path

from booker_api import views
from booker_api.apps import BookerApiConfig as AppConfig

API_VERSION_PREFIX = "v1"

app_name = AppConfig.name

urlpatterns = [
    re_path(
        fr"^{API_VERSION_PREFIX}/booking/$", views.BookingView.as_view(), name="booking"
    ),
    re_path(fr"^{API_VERSION_PREFIX}/slot/$", views.slot_list, name="slot-list"),
    re_path(fr"^{API_VERSION_PREFIX}/health/$", views.slot_list, name="health"),
]
