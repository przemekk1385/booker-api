import http

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_ok(authenticated_api_client):
    response = authenticated_api_client.get(reverse("operator_api:health"))

    assert response.status_code == http.HTTPStatus.OK, response.json()


def test_get_forbidden(api_client):
    response = api_client.get(reverse("operator_api:health"))

    assert response.status_code == http.HTTPStatus.FORBIDDEN, response.json()
