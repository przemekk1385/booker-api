import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_get_ok(authenticated_api_client):
    response = authenticated_api_client.get(reverse("operator_api:health"))

    assert response.status_code == status.HTTP_200_OK, response.json()


def test_get_forbidden(api_client):
    response = api_client.get(reverse("operator_api:health"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()
