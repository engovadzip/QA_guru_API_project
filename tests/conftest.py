import pytest


@pytest.fixture(autouse=True)
def BASE_URL():
    return 'https://restful-booker.herokuapp.com/'
