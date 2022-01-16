from unittest.mock import Mock, PropertyMock

from booker_api.utils import make_code


def test_make_code(faker, mocker):
    method_calls = faker.pyint(5, 10)

    mocked_objects = Mock()
    mocked_objects.filter.return_value.exists.side_effect = (method_calls - 1) * [
        True
    ] + [False]

    mocked_apartment = Mock()
    type(mocked_apartment).objects = PropertyMock(return_value=mocked_objects)

    mocker.patch("booker_api.utils.Apartment", mocked_apartment)

    assert make_code()
    assert len(mocked_objects.method_calls) == method_calls
