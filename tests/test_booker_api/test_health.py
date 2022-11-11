from django.urls import reverse
from rest_framework import status


def test_health(api_client):
    response = api_client.get(reverse("booker_api:health"))

    assert response.status_code == status.HTTP_200_OK
