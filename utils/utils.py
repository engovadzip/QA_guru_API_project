from allure_commons.types import AttachmentType
from random import randint
import logging

import json
import os
import allure
import requests
import jsonschema


def load_schema(filepath):
    with open(os.path.dirname(os.path.abspath(__file__)) + '/schemas/' + filepath) as file:
        schema = json.load(file)
        return schema


def user(username, passw):
    info = {
        "username": f"{username}",
        "password": f"{passw}"
    }

    return info


def attachment(response):
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                  attachment_type=AttachmentType.JSON, extension="json")
    allure.attach(body=str(response.status_code), name="Response status code", attachment_type=AttachmentType.TEXT,
                  extension="txt")


def get_token(link, user_name, password):
    token_schema = load_schema('get_token.json')

    with allure.step("Отправка запроса на получение токена"):
        response = requests.post(url=link + URL.token_url, data=user(user_name, password))

    with allure.step("Проверка корректности запроса"):
        assert response.status_code == 200

    with allure.step("Валидация .json ответа"):
        jsonschema.validate(response.json(), token_schema)

    attachment(response)

    token = response.json()["token"]

    assert token is not None
    assert token != ''

    logging.info(response.request.url)
    logging.info(response.status_code)
    logging.info(response.text)

    return token


def get_random_booking_id(BASE_URL):
    response = requests.get(url=BASE_URL + URL.booking_url)
    booking_schema = load_schema('get_bookings.json')

    with allure.step("Проверка корректности запроса"):
        assert response.status_code == 200

    with allure.step("Валидация первой брони из .json ответа"):
        booking_response = response.json()[0]
        jsonschema.validate(booking_response, booking_schema)

    n = len(response.json())
    n = randint(0, n - 1)
    booking_id = response.json()[n]['bookingid']

    allure.attach(body=str(booking_id), name="Booking ID", attachment_type=AttachmentType.TEXT,
                  extension="txt")

    return booking_id


class URL:
    token_url = 'auth/'

    booking_url = 'booking/'