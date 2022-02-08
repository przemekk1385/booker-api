import http
from datetime import date, timedelta

import pytest
from django.urls import reverse

from booker_api.models import Booking


@pytest.mark.django_db
def test_list_ok(apartment_instance, authenticated_api_client, faker):
    total_bookings = 5
    slots = [slot.value for slot in Booking.Slot]
    for slot in faker.random_elements(
        elements=slots, length=total_bookings, unique=True
    ):
        Booking.objects.create(
            apartment=apartment_instance,
            day=date.today() + timedelta(days=1),
            slot=slot,
        )

    response = authenticated_api_client.get(reverse("operator_api:booking-list"))

    assert response.status_code == http.HTTPStatus.OK, response.json()
    assert len(response.json()) == Booking.objects.count()


@pytest.mark.django_db
def test_list_not_authenticated(authenticated_api_client, user_instance):
    user_instance.groups.set([])
    response = authenticated_api_client.get(reverse("operator_api:booking-list"))

    assert response.status_code == http.HTTPStatus.FORBIDDEN, response.json()
