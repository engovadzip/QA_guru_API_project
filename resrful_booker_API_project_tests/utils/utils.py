from allure_commons.types import AttachmentType
from pathlib import Path
from random import randint
import logging
import json
import allure
import requests
import jsonschema

token_url = 'auth/'
booking_url = 'booking/'


def path(schema_name):
    return str(Path(__file__).parent.parent.parent.joinpath(f'schemas/{schema_name}'))


def load_schema(filepath):
    with open(path(filepath)) as file:
        schema = json.load(file)
        return schema


def user(username, passw):
    info = {
        "username": f"{username}",
        "password": f"{passw}"
    }

    return info


def get_token(link, user_name, password):
    token_schema = load_schema('get_token.json')

    with allure.step("Отправка запроса на получение токена"):
        response = requests.post(url=link + token_url, data=user(user_name, password))

    with allure.step("Проверка корректности запроса"):
        assert response.status_code == 200

    with allure.step("Валидация .json ответа"):
        jsonschema.validate(response.json(), token_schema)

    allure.attach(body=response.request.url, name="Request URL", attachment_type=AttachmentType.TEXT)
    allure.attach(body=response.request.method, name="Request method", attachment_type=AttachmentType.TEXT)
    allure.attach(body=str(response.status_code), name="Response status code", attachment_type=AttachmentType.TEXT,
                  extension='txt')
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response body",
                  attachment_type=AttachmentType.JSON, extension="json")
    logging.info("Request: " + response.request.url)
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)

    token = response.json()["token"]

    assert token is not None
    assert token != ''

    return token


def get_random_booking_id(url):
    response = requests.get(url=url + booking_url)
    booking_schema = load_schema('get_bookings.json')

    with allure.step("Проверка корректности запроса"):
        assert response.status_code == 200

    with allure.step("Валидация первой брони из .json ответа"):
        booking_response = response.json()[0]
        jsonschema.validate(booking_response, booking_schema)

    n = len(response.json())
    n = randint(0, n - 1)
    booking_id = response.json()[n]['bookingid']

    allure.attach(body=response.request.url, name="Request URL", attachment_type=AttachmentType.TEXT)
    allure.attach(body=response.request.method, name="Request method", attachment_type=AttachmentType.TEXT)
    allure.attach(body=str(response.status_code), name="Response status code", attachment_type=AttachmentType.TEXT,
                  extension='txt')
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response body",
                  attachment_type=AttachmentType.JSON, extension="json")
    logging.info("Request: " + response.request.url)
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)

    return booking_id
