import http
from datetime import date, timedelta

import pytest
from django.urls import reverse

from golden_view_wellness_api.models import Booking, Stay


@pytest.mark.django_db
def test_list(api_client, faker):
    days = 3

    stay_instance = Stay.objects.create(
        apartment=Stay.Apartment.APARTMENT_1,
        date_from=date.today(),
        date_to=date.today() + timedelta(days=days),
        identifier=faker.numerify("#########"),
    )

    for i in range(days):
        Booking.objects.create(
            stay=stay_instance,
            day=stay_instance.date_from + timedelta(days=i),
            slot=faker.random_element(Booking.Slot),
        )

    response = api_client.get(reverse("golden_view_wellness_api:booking-list"))

    assert response.status_code == http.HTTPStatus.OK
    assert len(response.json()) == days


@pytest.mark.django_db
def test_create(api_client, faker):
    stay_instance = Stay.objects.create(
        apartment=Stay.Apartment.APARTMENT_1,
        date_from=date.today(),
        date_to=date.today() + timedelta(days=3),
        identifier=faker.numerify("#########"),
    )

    payload = {
        "day": date.today(),
        "identifier": stay_instance.identifier,
        "slot": Booking.Slot.FROM11,
    }

    response = api_client.post(
        reverse("golden_view_wellness_api:booking-list"), payload
    )

    assert response.status_code == http.HTTPStatus.CREATED, response.json()
    assert response.json()["apartment"] == Stay.Apartment.APARTMENT_1.label
    assert response.json()["slot"] == Booking.Slot.FROM11.label
