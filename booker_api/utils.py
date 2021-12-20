from datetime import datetime

import pytz

timezone = pytz.timezone("Europe/Warsaw")


def get_now() -> datetime:
    return datetime.utcnow().astimezone(timezone)
