from datetime import date, timedelta

import pytest
from rest_framework.test import APIClient

from booker_api.models import Apartment, Booking
from operator_api.models import User


@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def authenticated_api_client(api_client, user_instance) -> APIClient:
    api_client.force_authenticate(user_instance)
    yield api_client


@pytest.fixture
def apartment_instance(faker) -> Apartment:
    return faker.random_element(Apartment.objects.all())


@pytest.fixture
def booking_instance(apartment_instance, faker) -> Booking:
    return Booking.objects.create(
        apartment=apartment_instance,
        day=date.today() + timedelta(days=1),
        slot=faker.random_element(Booking.Slot),
    )


@pytest.fixture
def user_instance(faker) -> User:
    user = User.objects.create_user(email=faker.email(), password=faker.word())
    user.apartments.set(Apartment.objects.all())
    return user
