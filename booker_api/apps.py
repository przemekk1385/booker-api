import environ
from django.apps import AppConfig

env = environ.Env(
    B_CODE_LENGTH=(int, 4),
    B_DAYS_BETWEEN=(int, 1),
)


class BookerApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "booker_api"
    code_length = env("B_CODE_LENGTH")
    days_between_bookings = env("B_DAYS_BETWEEN")
