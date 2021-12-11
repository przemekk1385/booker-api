from datetime import date, timedelta
from typing import Callable

import pytest
from rest_framework.test import APIClient

from booker_api.models import Apartment, Stay
from tests.constants import STAY_DAYS


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


@pytest.fixture()
def make_stay_instance(faker) -> Callable[[], Stay]:
    def _make_stay_instance(
        apartment: Apartment = None, date_from: date = None
    ) -> Stay:
        date_from = date_from or date.today()
        return Stay.objects.create(
            apartment=apartment or faker.random_element(Apartment.objects.all()),
            date_from=date_from,
            date_to=date_from + timedelta(days=STAY_DAYS),
            identifier=faker.numerify("#########"),
        )

    return _make_stay_instance
