import http

import pytest
from django.urls import reverse

from booker_api.models import Apartment


@pytest.mark.django_db
def test_list_ok(authenticated_api_client):
    response = authenticated_api_client.get(reverse("operator_api:apartment-list"))

    assert response.status_code == http.HTTPStatus.OK, response.json()
    assert len(response.json()) == Apartment.objects.count()


def test_list_faile(api_client):
    response = api_client.get(reverse("operator_api:apartment-list"))

    assert response.status_code == http.HTTPStatus.FORBIDDEN, response.json()
