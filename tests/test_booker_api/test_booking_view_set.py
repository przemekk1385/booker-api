import http
from datetime import date, datetime, timedelta
from unittest.mock import PropertyMock

import pytest
from django.apps import apps
from django.urls import reverse
from rest_framework.settings import api_settings

from booker_api.models import Booking


@pytest.mark.django_db
def test_list(api_client, faker, stay_instance):
    stay_instance.date_from = stay_instance.date_from - timedelta(days=2)
    stay_instance.save()
    total_bookings = (stay_instance.date_to - stay_instance.date_from).days

    for i in range(total_bookings):
        Booking.objects.create(
            stay=stay_instance,
            day=stay_instance.date_from + timedelta(days=i),
            slot=faker.random_element(Booking.Slot),
        )

    response = api_client.get(reverse("booker_api:booking-list"))

    assert response.status_code == http.HTTPStatus.OK, response.json()
    assert len(response.json()) == total_bookings - 1


@pytest.mark.django_db
def test_create_ok(api_client, faker, mocker, stay_instance):
    today = date.today()
    mocker.patch("booker_api.serializers.get_now").return_value = datetime(
        today.year, today.month, today.day, 10
    )
    mocker.patch.object(
        apps.get_app_config("booker_api"), "days_between_bookings", new=1
    )
    Booking.objects.create(
        stay=stay_instance,
        day=date.today() + timedelta(days=1),
        slot=faker.random_element(Booking.Slot),
    )

    payload = {
        "day": date.today(),
        "identifier": stay_instance.identifier,
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == http.HTTPStatus.CREATED, response.json()

    response_data = response.json()
    assert response_data["apartment"] == stay_instance.apartment.label
    assert response_data["slot"] == payload["slot"]
    assert response_data["slot_label"] == payload["slot"].label


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
def test_create_last_day(api_client, faker, stay_instance):
    payload = {
        "day": stay_instance.date_to,
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
        apps.get_app_config("booker_api"), "days_between_bookings", new=2
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


@pytest.mark.parametrize(
    "hour",
    (20, 21, 22, 23),
)
@pytest.mark.django_db
def test_create_after_8_p_m(hour, api_client, faker, mocker, stay_instance):
    today = date.today()
    mocker.patch("booker_api.serializers.get_now").return_value = datetime(
        today.year, today.month, today.day, hour
    )

    payload = {
        "day": date.today(),
        "identifier": stay_instance.identifier,
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == http.HTTPStatus.BAD_REQUEST, response.json()
    assert api_settings.NON_FIELD_ERRORS_KEY in response.json().keys()


@pytest.mark.parametrize(
    "hour",
    (11, 12, 13, 14, 15, 16, 17, 18, 19),
)
@pytest.mark.django_db
def test_create_hour_has_passed(hour, api_client, faker, mocker, stay_instance):
    today = date.today()
    mocker.patch("booker_api.serializers.get_now").return_value = datetime(
        today.year, today.month, today.day, hour
    )

    payload = {
        "day": date.today(),
        "identifier": stay_instance.identifier,
        "slot": hour - 1,
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == http.HTTPStatus.BAD_REQUEST, response.json()
    assert "slot" in response.json().keys()
