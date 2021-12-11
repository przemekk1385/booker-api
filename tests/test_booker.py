from booker_api import __version__ as booker_api_version
from operator_api import __version__ as operator_api_version


def test_version():
    assert booker_api_version == "0.1.0"
    assert operator_api_version == "0.1.0"
