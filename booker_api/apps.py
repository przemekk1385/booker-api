import environ
from django.apps import AppConfig

env = environ.Env(
    CODE_LENGTH=(int, 4),
    DAYS_BETWEEN=(int, 1),
)


class BookerApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "booker_api"
    code_length = env("CODE_LENGTH")
    days_between_bookings = env("DAYS_BETWEEN")
