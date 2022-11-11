from datetime import date, datetime, timedelta

import pytest
from django.apps import apps
from django.urls import reverse
from rest_framework import status
from rest_framework.settings import api_settings

from booker_api.models import Booking
from booker_api.utils import timezone


@pytest.mark.django_db
def test_list(apartment_instance, api_client, faker):
    total_bookings = 7

    for i in range(total_bookings):
        Booking.objects.create(
            apartment=apartment_instance,
            day=date.today() + timedelta(days=i - 2),
            slot=faker.random_element(Booking.Slot),
        )

    response = api_client.get(reverse("booker_api:booking-list"))

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert len(response.json()) == total_bookings - 1


@pytest.mark.django_db
def test_create_ok(apartment_instance, api_client, faker, mocker):
    today = date.today()
    mocker.patch("booker_api.serializers.get_now").return_value = datetime(
        today.year, today.month, today.day, 0
    ).astimezone(timezone)
    mocker.patch.object(
        apps.get_app_config("booker_api"), "days_between_bookings", new=1
    )
    Booking.objects.create(
        apartment=apartment_instance,
        day=date.today() + timedelta(days=1),
        slot=faker.random_element(Booking.Slot),
    )

    payload = {
        "code": apartment_instance.code,
        "day": date.today(),
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == status.HTTP_201_CREATED, response.json()

    response_data = response.json()
    assert response_data["apartment"] == apartment_instance.number
    assert response_data["slot"] == payload["slot"]


@pytest.mark.django_db
def test_create_day_already_passed(apartment_instance, api_client, faker):
    payload = {
        "code": apartment_instance.code,
        "day": date.today() - timedelta(days=99),
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert "day" in response.json().keys()


@pytest.mark.django_db
def test_create_no_code(api_client, faker):
    payload = {
        "code": faker.numerify("####"),
        "day": date.today() + timedelta(days=1),
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.json()


@pytest.mark.parametrize("timedelta_days", (1, 3))
@pytest.mark.django_db
def test_create_booking_not_possible(
    timedelta_days, apartment_instance, api_client, faker, mocker
):
    mocker.patch.object(
        apps.get_app_config("booker_api"), "days_between_bookings", new=2
    )
    Booking.objects.create(
        apartment=apartment_instance,
        day=date.today() + timedelta(days=2),
        slot=faker.random_element(Booking.Slot),
    )

    payload = {
        "code": apartment_instance.code,
        "day": date.today() + timedelta(days=timedelta_days),
        "slot": faker.random_element(Booking.Slot),
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert "day" in response.json().keys()


@pytest.mark.django_db
def test_create_day_slot_exist(api_client, booking_instance):
    payload = {
        "code": booking_instance.apartment.code,
        "day": booking_instance.day,
        "slot": booking_instance.slot,
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert api_settings.NON_FIELD_ERRORS_KEY in response.json().keys()


@pytest.mark.parametrize("slot", (20, 21))
@pytest.mark.django_db
def test_create_after_8_p_m(slot, apartment_instance, api_client, faker, mocker):
    payload = {
        "code": apartment_instance.code,
        "day": date.today(),
        "slot": slot,
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert "slot" in response.json().keys()


@pytest.mark.parametrize("hour", (11, 12, 13, 14, 15, 16, 17, 18, 19))
@pytest.mark.django_db
def test_create_hour_has_passed(hour, apartment_instance, api_client, mocker):
    today = date.today()
    mocker.patch("booker_api.serializers.get_now").return_value = datetime(
        today.year, today.month, today.day, hour
    )

    payload = {
        "day": date.today(),
        "code": apartment_instance.code,
        "slot": hour - 1,
    }

    response = api_client.post(reverse("booker_api:booking-list"), payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert "slot" in response.json().keys()


@pytest.mark.parametrize("timedelta_days,hour", ((1, 22), (0, 10)))
@pytest.mark.django_db
def test_cancel_day_before_ok(
    hour, timedelta_days, api_client, booking_instance, mocker
):
    booking_day = booking_instance.day - timedelta(days=timedelta_days)
    mocker.patch("booker_api.viewsets.get_now").return_value = datetime(
        booking_day.year, booking_day.month, booking_day.day, hour
    )

    payload = {
        "day": booking_instance.day,
        "code": booking_instance.apartment.code,
    }

    response = api_client.post(reverse("booker_api:booking-cancel"), payload)

    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()


@pytest.mark.parametrize(
    "payload,error_in",
    (
        ({}, {"code", "day"}),
        ({"day": date.today()}, {"code"}),
        ({"code": ""}, {"day"}),
    ),
)
@pytest.mark.django_db
def test_cancel_bad_request(payload, error_in, api_client):
    response = api_client.post(reverse("booker_api:booking-cancel"), payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert not error_in.difference(response.json().keys())


@pytest.mark.parametrize("hour", (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21))
@pytest.mark.django_db
def test_cancel_hour_has_passed(
    hour, apartment_instance, api_client, booking_instance, mocker
):
    booking_instance.slot = Booking.Slot(hour)
    booking_instance.save()

    booking_day = booking_instance.day
    mocker.patch("booker_api.viewsets.get_now").return_value = datetime(
        booking_day.year, booking_day.month, booking_day.day, hour - 1, 30
    )

    payload = {
        "day": booking_instance.day,
        "code": apartment_instance.code,
    }

    response = api_client.post(reverse("booker_api:booking-cancel"), payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()
    assert api_settings.NON_FIELD_ERRORS_KEY in response.json().keys()
