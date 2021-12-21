from datetime import date, timedelta
from typing import Callable

import pytest
from rest_framework.test import APIClient

from booker_api.models import Apartment, Booking, Stay
from operator_api.models import User
from tests.constants import STAY_DAYS


@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user_instance) -> APIClient:
    api_client.force_authenticate(user_instance)
    yield api_client


@pytest.fixture
def booking_instance(faker, stay_instance) -> Booking:
    return Booking.objects.create(
        stay=stay_instance,
        day=stay_instance.date_from + timedelta(days=1),
        slot=faker.random_element(Booking.Slot),
    )


@pytest.fixture
def stay_instance(faker) -> Stay:
    return Stay.objects.create(
        apartment=faker.random_element(Apartment.objects.all()),
        date_from=date.today(),
        date_to=date.today() + timedelta(days=STAY_DAYS),
        identifier=faker.numerify("#########"),
    )


@pytest.fixture
def user_instance(faker) -> User:
    user = User.objects.create_user(email=faker.email(), password=faker.word())
    user.apartments.set(Apartment.objects.all())
    return user


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
