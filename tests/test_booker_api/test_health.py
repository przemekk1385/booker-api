import http

from django.urls import reverse


def test_health(api_client):
    response = api_client.get(reverse("booker_api:health"))

    assert response.status_code == http.HTTPStatus.OK
