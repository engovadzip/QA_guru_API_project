import allure
import requests
import jsonschema
from utils.utils import attachment, load_schema, get_token, get_random_booking_id, URL
from allure_commons.types import AttachmentType
import json


@allure.story("Получение токена для возможности редактирования бронирования.")
def test_create_token(BASE_URL):
    token = get_token(BASE_URL)

    assert token is not None
    assert token != ''


@allure.story("Получение списка с id бронирований.")
def test_get_bookings(BASE_URL):
    booking_schema = load_schema('get_bookings.json')
    response = requests.get(url=BASE_URL + URL.get_bookings)

    with allure.step("Проверка корректности запроса"):
        assert response.status_code == 200

    with allure.step("Валидация первой брони из .json ответа"):
        booking_response = response.json()[0]
        jsonschema.validate(booking_response, booking_schema)

    attachment(response)


@allure.story("Получение информации о бронировании.")
def test_get_booking_info(BASE_URL):
    with allure.step("Получение id одного из случайных бронирований"):
        booking_id = str(get_random_booking_id(BASE_URL))

    response = requests.get(url=BASE_URL + URL.get_bookings + booking_id)

    with allure.step("Проверка корректности запроса"):
        assert response.status_code == 200

    with allure.step("Валидация .json ответа"):
        booking_info_schema = load_schema('get_booking_info.json')
        jsonschema.validate(response.json(), booking_info_schema)

    attachment(response)
