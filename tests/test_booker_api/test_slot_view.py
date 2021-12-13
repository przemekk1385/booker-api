import http

import pytest
from django.urls import reverse

from booker_api.models import Booking


@pytest.mark.django_db
def test_list_ok(authenticated_api_client):
    response = authenticated_api_client.get(reverse("booker_api:slot-list"))

    assert response.status_code == http.HTTPStatus.OK, response.json()
    assert len(response.json()) == len(Booking.Slot)
