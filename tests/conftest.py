import os
import pytest
from dotenv import load_dotenv, find_dotenv


@pytest.fixture(scope='session', autouse=True)
def load_env():
    find_dotenv()
    load_dotenv()


@pytest.fixture(scope='function')
def booking_info():
    info = {
        "firstname": os.getenv("FIRSTNAME"),
        "lastname": os.getenv("LASTNAME"),
        "totalprice": int(os.getenv("TOTALPRICE")),
        "depositpaid": bool(os.getenv("DEPOSITPAID")),
        "bookingdates": {
            "checkin": os.getenv("CHECKIN"),
            "checkout": os.getenv("CHECKOUT")

        },
        "additionalneeds": os.getenv("ADDITIONALNEEDS")
    }
    return info


@pytest.fixture(scope='function')
def base_url():
    URL = os.getenv('BASE_URL')
    return URL


@pytest.fixture(scope='function')
def user_name():
    username = os.getenv('USER')
    return username


@pytest.fixture(scope='function')
def password():
    password = os.getenv('PASSWORD')
    return password
