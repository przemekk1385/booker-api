import secrets
import string

import pytz
from django.apps import apps
from django.utils.datetime_safe import datetime

from booker_api.models import Apartment

alphabet = string.digits
code_length = apps.get_app_config("booker_api").code_length
timezone = pytz.timezone("Europe/Warsaw")


def get_now() -> datetime:
    return datetime.utcnow().astimezone(timezone)


def make_code() -> str:
    code = None
    while code is None or Apartment.objects.filter(code=code).exists():
        code = "".join(secrets.choice(alphabet) for _ in range(code_length))
    return code
