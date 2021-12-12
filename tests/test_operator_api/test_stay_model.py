from datetime import date, timedelta

import pytest
from django.db import IntegrityError

from booker_api.models import Apartment, Stay


@pytest.mark.django_db
def test_unique_constraint(faker):
    stay_instance = Stay.objects.create(
        apartment=faker.random_element(Apartment.objects.all()),
        identifier=faker.numerify("#########"),
        date_from=date.today(),
        date_to=date.today() + timedelta(days=7),
    )

    with pytest.raises(IntegrityError):
        Stay.objects.create(
            apartment=stay_instance.apartment,
            identifier=faker.numerify("#########"),
            date_from=stay_instance.date_from,
            date_to=stay_instance.date_to,
        )
