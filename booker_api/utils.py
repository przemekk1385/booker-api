import pytz
from django.utils.datetime_safe import datetime

timezone = pytz.timezone("Europe/Warsaw")


def get_now() -> datetime:
    return datetime.utcnow().astimezone(timezone)
