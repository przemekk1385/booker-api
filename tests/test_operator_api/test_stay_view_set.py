import http
from datetime import date, timedelta

import pytest
from django.urls import reverse

from booker_api.models import Apartment, Stay
from tests import constants


@pytest.mark.django_db
def test_list_ok(authenticated_api_client, make_stay_instance, user_instance):
    for i in range(3):
        make_stay_instance(
            date_from=date.today() + timedelta(days=i * constants.STAY_DAYS)
        )

    response = authenticated_api_client.get(reverse("operator_api:stay-list"))

    assert response.status_code == http.HTTPStatus.OK, response.json()
    assert len(response.json()) == Stay.objects.count()


@pytest.mark.django_db
def test_list_failed(api_client):
    response = api_client.get(reverse("operator_api:stay-list"))

    assert response.status_code == http.HTTPStatus.FORBIDDEN, response.json()


@pytest.mark.django_db
def test_create_ok(authenticated_api_client, faker, user_instance):
    payload = {
        "apartment": faker.random_element(Apartment.objects.all()).id,
        "date_from": date.today(),
        "date_to": date.today() + timedelta(days=constants.STAY_DAYS),
        "identifier": faker.numerify("#########"),
    }

    response = authenticated_api_client.post(reverse("operator_api:stay-list"), payload)

    assert response.status_code == http.HTTPStatus.CREATED, response.json()
    assert set(response.json().keys()).difference(payload.keys()) == {"id"}


@pytest.mark.django_db
def test_create_failed(authenticated_api_client, faker, user_instance):
    payload = {
        "apartment": faker.random_element(Apartment.objects.all()).id,
        "date_from": date.today(),
        "date_to": date.today() + timedelta(days=constants.STAY_DAYS),
        "identifier": faker.numerify("#########"),
    }
    user_instance.apartments.remove(payload["apartment"])

    response = authenticated_api_client.post(reverse("operator_api:stay-list"), payload)

    assert response.status_code == http.HTTPStatus.FORBIDDEN, response.json()


@pytest.mark.django_db
def test_retrieve_ok(authenticated_api_client, stay_instance):
    response = authenticated_api_client.get(
        reverse("operator_api:stay-detail", args=[stay_instance.id])
    )

    assert response.status_code == http.HTTPStatus.OK, response.json()

    response_data = response.json()
    assert response_data["id"] == stay_instance.id
    assert response_data["apartment"] == stay_instance.apartment.id
    assert response_data["identifier"] == stay_instance.identifier
    assert "date_from" in response_data.keys()
    assert "date_to" in response_data.keys()


@pytest.mark.django_db
def test_retrieve_failed(api_client, stay_instance):
    response = api_client.get(
        reverse("operator_api:stay-detail", args=[stay_instance.id])
    )

    assert response.status_code == http.HTTPStatus.FORBIDDEN, response.json()


@pytest.mark.django_db
def test_update_ok(authenticated_api_client, faker, stay_instance, user_instance):
    prev_identifier = stay_instance.identifier
    payload = {"identifier": faker.numerify("#########")}

    response = authenticated_api_client.patch(
        reverse("operator_api:stay-detail", args=[stay_instance.id]), payload
    )

    assert response.status_code == http.HTTPStatus.OK, response.json()

    response_data = response.json()
    assert response_data["identifier"] == payload["identifier"] != prev_identifier


@pytest.mark.django_db
def test_update_failed(authenticated_api_client, faker, stay_instance, user_instance):
    payload = {"identifier": faker.numerify("#########")}
    user_instance.apartments.remove(stay_instance.apartment)

    response = authenticated_api_client.patch(
        reverse("operator_api:stay-detail", args=[stay_instance.id]), payload
    )

    assert response.status_code == http.HTTPStatus.FORBIDDEN, response.json()


@pytest.mark.django_db
def test_delete_ok(authenticated_api_client, stay_instance):
    response = authenticated_api_client.delete(
        reverse("operator_api:stay-detail", args=[stay_instance.id])
    )

    assert response.status_code == http.HTTPStatus.NO_CONTENT, response.json()
    assert not Stay.objects.exists()


@pytest.mark.django_db
def test_delete_failed(authenticated_api_client, stay_instance, user_instance):
    user_instance.apartments.remove(stay_instance.apartment)

    response = authenticated_api_client.delete(
        reverse("operator_api:stay-detail", args=[stay_instance.id])
    )

    assert response.status_code == http.HTTPStatus.FORBIDDEN, response.json()
