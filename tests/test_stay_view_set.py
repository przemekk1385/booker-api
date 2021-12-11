import http
from datetime import date, timedelta

import pytest
from django.urls import reverse

from booker_api.models import Apartment, Stay
from tests import constants


@pytest.mark.django_db
def test_list(api_client, make_stay_instance):
    for i in range(3):
        make_stay_instance(
            date_from=date.today() + timedelta(days=i * constants.STAY_DAYS)
        )

    response = api_client.get(reverse("operator_api:stay-list"))

    assert response.status_code == http.HTTPStatus.OK, response.json()
    assert len(response.json()) == Stay.objects.count()


@pytest.mark.django_db
def test_create(api_client, faker):
    payload = {
        "apartment": faker.random_element(Apartment.objects.all()).id,
        "date_from": date.today(),
        "date_to": date.today() + timedelta(days=constants.STAY_DAYS),
        "identifier": faker.numerify("#########"),
    }

    response = api_client.post(reverse("operator_api:stay-list"), payload)

    assert response.status_code == http.HTTPStatus.CREATED, response.json()
    assert set(response.json().keys()).difference(payload.keys()) == {"id"}


@pytest.mark.django_db
def test_retrieve(api_client, stay_instance):
    response = api_client.get(
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
def test_update(api_client, faker, stay_instance):
    prev_identifier = stay_instance.identifier
    payload = {"identifier": faker.numerify("#########")}

    response = api_client.patch(
        reverse("operator_api:stay-detail", args=[stay_instance.id]), payload
    )

    assert response.status_code == http.HTTPStatus.OK, response.json()

    response_data = response.json()
    assert response_data["identifier"] == payload["identifier"] != prev_identifier


@pytest.mark.django_db
def test_delete(api_client, stay_instance):
    response = api_client.delete(
        reverse("operator_api:stay-detail", args=[stay_instance.id])
    )

    assert response.status_code == http.HTTPStatus.NO_CONTENT
    assert not Stay.objects.exists()
