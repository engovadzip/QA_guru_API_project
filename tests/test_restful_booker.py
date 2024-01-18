import allure
import requests
import jsonschema
from ..restful_booker_API_project_tests.utils.utils import load_schema, get_token, get_random_booking_id
from ..restful_booker_API_project_tests.utils.api_methods import (create_booking, delete_booking, get_booikngs,
                                                                  get_booikng_info, update_booikng)
from allure_commons.types import AttachmentType
import json
import logging

token_url = 'auth/'
booking_url = 'booking/'


@allure.story("Получение токена для возможности редактирования бронирования")
def test_create_token(base_url, user_name, password):
    get_token(base_url, user_name, password)


@allure.story("Получение списка с id бронирований")
def test_get_bookings(base_url):
    booking_schema = load_schema('get_bookings.json')

    with allure.step("Получение списка с id бронирований"):
        response = get_booikngs(base_url)

    with allure.step("Проверка ответа запроса"):
        assert response.status_code == 200

    with allure.step("Валидация первой брони из .json ответа"):
        booking_response = response.json()[0]
        jsonschema.validate(booking_response, booking_schema)


@allure.story("Получение информации о бронировании")
def test_get_booking_info(base_url):
    with allure.step("Получение id одного из случайных бронирований"):
        booking_id = str(get_random_booking_id(base_url))

    with allure.step(f"Получение информации о бронировании {booking_id}"):
        response = get_booikng_info(base_url, booking_id)

    with allure.step("Проверка ответа запроса"):
        assert response.status_code == 200

    with allure.step("Валидация .json ответа"):
        booking_info_schema = load_schema('get_booking_info.json')
        jsonschema.validate(response.json(), booking_info_schema)


@allure.story("Полное изменение информации о бронировании")
def test_update_booking_info(base_url, booking_info, user_name, password):
    with allure.step("Получение токена для возможности редактирования бронирования"):
        token = get_token(base_url, user_name, password)

    with allure.step("Получение id одного из случайных бронирований"):
        booking_id = str(get_random_booking_id(base_url))

        response = get_booikng_info(base_url, booking_id)

        with allure.step("Проверка ответа запроса"):
            assert response.status_code == 200

        with allure.step("Валидация .json ответа"):
            booking_info_schema = load_schema('get_booking_info.json')
            jsonschema.validate(response.json(), booking_info_schema)

    with allure.step(f"Обновление информации в бронировании {booking_id}"):
        update_response = update_booikng(base_url, booking_id, booking_info, token)

    with allure.step("Проверка ответа запроса"):
        assert update_response.status_code == 200

    with allure.step("Валидация .json ответа"):
        upd_booking_info_schema = load_schema('get_booking_info.json')
        jsonschema.validate(update_response.json(), upd_booking_info_schema)

    with allure.step("Получение информации об обновленном бронировании"):
        upd_response = get_booikng_info(base_url, booking_id)

        with allure.step("Проверка ответа запроса"):
            assert update_response.status_code == 200

        with allure.step("Валидация .json ответа"):
            upd_booking_info_schema = load_schema('get_booking_info.json')
            jsonschema.validate(update_response.json(), upd_booking_info_schema)

        with allure.step("Проверка соответствия информации в бронировании"):
            assert booking_info == upd_response.json()


@allure.story("Создание нового бронирования")
def test_create_booking(base_url, booking_info):
    with allure.step("Отправка запроса с данными о новом бронировании"):
        response = create_booking(base_url, booking_info)

        with allure.step("Проверка ответа запроса"):
            assert response.status_code == 200

        with allure.step("Валидация .json ответа"):
            booking_info_schema = load_schema('post_booking.json')
            jsonschema.validate(response.json(), booking_info_schema)

    with allure.step("Получение id созданного бронирования"):
        booking_id = str(response.json()['bookingid'])

    with allure.step("Получение информации о созданном бронировании"):
        upd_response = get_booikng_info(base_url, booking_id)

        with allure.step("Проверка ответа запроса"):
            assert upd_response.status_code == 200

        with allure.step("Валидация .json ответа"):
            new_booking_info_schema = load_schema('get_booking_info.json')
            jsonschema.validate(upd_response.json(), new_booking_info_schema)

        with allure.step("Проверка соответствия информации в созданном бронировании"):
            assert booking_info == upd_response.json()


@allure.story("Удаление случайного бронирования")
def test_delete_booking(base_url, user_name, password):
    with allure.step("Получение токена для возможности редактирования бронирования"):
        token = get_token(base_url, user_name, password)

    with allure.step("Получение id одного из случайных бронирований"):
        booking_id = str(get_random_booking_id(base_url))

        response = get_booikng_info(base_url, booking_id)

        with allure.step("Проверка ответа запроса"):
            assert response.status_code == 200

        with allure.step("Валидация .json ответа"):
            booking_info_schema = load_schema('get_booking_info.json')
            jsonschema.validate(response.json(), booking_info_schema)

    with allure.step(f"Удаление бронирования {booking_id}"):
        delete_response = delete_booking(base_url, booking_id, token)

    with allure.step("Проверка ответа запроса"):
        assert delete_response.status_code == 201
