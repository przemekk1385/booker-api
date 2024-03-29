import pytest
from django.urls import reverse
from rest_framework import status

from booker_api.models import Apartment


@pytest.mark.django_db
def test_list_ok(authenticated_api_client, user_instance):
    response = authenticated_api_client.get(reverse("operator_api:apartment-list"))

    assert response.status_code == status.HTTP_200_OK, response.json()
    assert (
        len(response.json())
        == Apartment.objects.filter(operators=user_instance).count()
    )


@pytest.mark.django_db
def test_list_not_authenticated(api_client):
    response = api_client.get(reverse("operator_api:apartment-list"))

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()


@pytest.mark.django_db
def test_create_method_not_allowed(authenticated_api_client):
    response = authenticated_api_client.post(reverse("operator_api:apartment-list"), {})

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, response.json()
    assert "POST" in response.json()["detail"]


@pytest.mark.django_db
def test_retrieve_ok(apartment_instance, authenticated_api_client):
    response = authenticated_api_client.get(
        reverse("operator_api:apartment-detail", args=[apartment_instance.id])
    )

    assert response.status_code == status.HTTP_200_OK, response.json()

    response_data = response.json()
    assert response_data["id"] == apartment_instance.id
    assert response_data["code"] == apartment_instance.code
    assert response_data["number"] == apartment_instance.number


@pytest.mark.django_db
def test_retrieve_not_is_operator(
    apartment_instance, authenticated_api_client, user_instance
):
    user_instance.apartments.remove(apartment_instance)

    response = authenticated_api_client.get(
        reverse("operator_api:apartment-detail", args=[apartment_instance.id])
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()


@pytest.mark.django_db
def test_update_method_not_allowed(apartment_instance, authenticated_api_client):
    response = authenticated_api_client.patch(
        reverse("operator_api:apartment-detail", args=[apartment_instance.id]), {}
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, response.json()
    assert "PATCH" in response.json()["detail"]


@pytest.mark.django_db
def test_delete_forbidden(apartment_instance, authenticated_api_client, user_instance):
    user_instance.apartments.remove(apartment_instance)

    response = authenticated_api_client.delete(
        reverse("operator_api:apartment-detail", args=[apartment_instance.id])
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()


@pytest.mark.django_db
def test_delete_method_not_allowed(
    apartment_instance, authenticated_api_client, user_instance
):
    response = authenticated_api_client.delete(
        reverse("operator_api:apartment-detail", args=[apartment_instance.id])
    )

    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, response.json()
    assert "DELETE" in response.json()["detail"]


@pytest.mark.django_db
def test_refresh_code_ok(apartment_instance, authenticated_api_client):
    prev_code = apartment_instance.code

    response = authenticated_api_client.post(
        reverse("operator_api:apartment-refresh-code", args=[apartment_instance.id])
    )

    assert response.status_code == status.HTTP_200_OK, response.json()

    response_data = response.json()
    assert prev_code != response_data["code"]


@pytest.mark.django_db
def test_refresh_code_forbidden(
    apartment_instance, authenticated_api_client, user_instance
):
    user_instance.apartments.remove(apartment_instance)

    response = authenticated_api_client.post(
        reverse("operator_api:apartment-refresh-code", args=[apartment_instance.id])
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()
