import http
from datetime import date, timedelta

import pytest
from django.apps import apps
from django.urls import reverse
from rest_framework.settings import api_settings

from booker_api.models import Booking, Stay

STAY_DAYS = 7


@pytest.fixture
def stay_instance(faker):
    return Stay.objects.create(
        apartment=faker.random_element(Stay.Apartment),
        date_from=date.today(),
        date_to=date.today() + timedelta(days=STAY_DAYS),
        identifier=faker.numerify("#########"),
    )


@pytest.mark.django_db
def test_list(api_client, faker, stay_instance):
    total_bookings = 3

    for i in range(total_bookings):
        Booking.objects.create(
            stay=stay_instance,
            day=stay_instance.date_from + timedelta(days=i + 1),
            slot=faker.random_element(Booking.Slot),
        )

    response = api_client.get(reverse("booker_api:booking-list"))

    assert response.status_code == http.HTTPStatus.OK, response.json()
    assert len(response.json()) == total_bookings


@pytest.mark.django_db
def test_create_ok(api_client, faker, stay_instance):
    payload = {
        "day": date.today() + timedelta(days=1),
        "identifier": stay_instance.identifier,
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == http.HTTPStatus.CREATED, response.json()
    assert response.json()["apartment"] == stay_instance.apartment.label
    assert response.json()["slot"] == payload["slot"]
    assert response.json()["slot_label"] == payload["slot"].label


@pytest.mark.django_db
def test_create_day_already_passed(api_client, faker, stay_instance):
    payload = {
        "day": date.today() - timedelta(days=99),
        "identifier": stay_instance.identifier,
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == http.HTTPStatus.BAD_REQUEST, response.json()
    assert "day" in response.json().keys()


@pytest.mark.django_db
def test_create_no_stay(api_client, faker):
    payload = {
        "day": date.today() + timedelta(days=1),
        "identifier": faker.numerify("#########"),
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == http.HTTPStatus.BAD_REQUEST, response.json()
    assert "identifier" in response.json().keys()


@pytest.mark.parametrize(
    "timedelta_days",
    (1, 3),
)
@pytest.mark.django_db
def test_create_booking_not_possible(
    timedelta_days, api_client, faker, mocker, stay_instance
):
    mocker.patch.object(
        apps.get_app_config("booker_api"), "days_between_bookings", new=1
    )
    Booking.objects.create(
        stay=stay_instance,
        day=date.today() + timedelta(days=2),
        slot=faker.random_element(Booking.Slot),
    )

    payload = {
        "day": date.today() + timedelta(days=timedelta_days),
        "identifier": stay_instance.identifier,
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == http.HTTPStatus.BAD_REQUEST, response.json()
    assert "day" in response.json().keys()


@pytest.mark.django_db
def test_create_day_slot_exist(api_client, faker, stay_instance):
    booking = Booking.objects.create(
        stay=stay_instance,
        day=date.today() + timedelta(days=1),
        slot=faker.random_element(Booking.Slot),
    )

    payload = {
        "day": booking.day,
        "identifier": stay_instance.identifier,
        "slot": booking.slot,
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == http.HTTPStatus.BAD_REQUEST, response.json()
    assert api_settings.NON_FIELD_ERRORS_KEY in response.json().keys()
