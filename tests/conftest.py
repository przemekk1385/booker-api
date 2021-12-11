from datetime import date, timedelta

import pytest
from rest_framework.test import APIClient

from booker_api.models import Apartment, Stay

STAY_DAYS: int = 7


@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def stay_instance(faker) -> Stay:
    return Stay.objects.create(
        apartment=faker.random_element(Apartment.objects.all()),
        date_from=date.today(),
        date_to=date.today() + timedelta(days=STAY_DAYS),
        identifier=faker.numerify("#########"),
    )
