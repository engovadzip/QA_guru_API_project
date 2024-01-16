import allure
import requests
import jsonschema
from utils.utils import attachment, load_schema, get_token, get_random_booking_id, URL
from allure_commons.types import AttachmentType
import json


@allure.story("Получение токена для возможности редактирования бронирования")
def test_create_token(base_URL, user_name, password):
    get_token(base_URL, user_name, password)


@allure.story("Получение списка с id бронирований")
def test_get_bookings(base_URL):
    booking_schema = load_schema('get_bookings.json')
    response = requests.get(url=base_URL + URL.booking_url)

    with allure.step("Проверка ответа запроса"):
        assert response.status_code == 200

    with allure.step("Валидация первой брони из .json ответа"):
        booking_response = response.json()[0]
        jsonschema.validate(booking_response, booking_schema)

    attachment(response)


@allure.story("Получение информации о бронировании")
def test_get_booking_info(base_URL):
    with allure.step("Получение id одного из случайных бронирований"):
        booking_id = str(get_random_booking_id(base_URL))

    response = requests.get(url=base_URL + URL.booking_url + booking_id)

    with allure.step("Проверка ответа запроса"):
        assert response.status_code == 200

    with allure.step("Валидация .json ответа"):
        booking_info_schema = load_schema('get_booking_info.json')
        jsonschema.validate(response.json(), booking_info_schema)

    attachment(response)


@allure.story("Полное изменение информации о бронировании")
def test_update_booking_info(base_URL, booking_info, user_name, password):
    with allure.step("Получение токена для возможности редактирования бронирования"):
        token = get_token(base_URL, user_name, password)

    with allure.step("Получение id одного из случайных бронирований"):
        booking_id = str(get_random_booking_id(base_URL))

        response = requests.get(url=base_URL + URL.booking_url + booking_id)

        with allure.step("Проверка ответа запроса"):
            assert response.status_code == 200

        with allure.step("Валидация .json ответа"):
            booking_info_schema = load_schema('get_booking_info.json')
            jsonschema.validate(response.json(), booking_info_schema)

    update_response = requests.put(url=base_URL + URL.booking_url + booking_id, json=booking_info,
                                   headers={"Cookie": f"token={token}"})

    with allure.step("Проверка ответа запроса"):
        assert update_response.status_code == 200

    with allure.step("Валидация .json ответа"):
        upd_booking_info_schema = load_schema('get_booking_info.json')
        jsonschema.validate(update_response.json(), upd_booking_info_schema)

    with allure.step("Получение информации об обновленном бронировании"):
        upd_response = requests.get(url=base_URL + URL.booking_url + booking_id)

        with allure.step("Проверка ответа запроса"):
            assert update_response.status_code == 200

        with allure.step("Валидация .json ответа"):
            upd_booking_info_schema = load_schema('get_booking_info.json')
            jsonschema.validate(update_response.json(), upd_booking_info_schema)

        with allure.step("Проверка соответствия информации в бронировании"):
            assert booking_info == upd_response.json()

    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response before update",
                  attachment_type=AttachmentType.JSON, extension="json")
    allure.attach(body=json.dumps(upd_response.json(), indent=4, ensure_ascii=True), name="Response after update",
                  attachment_type=AttachmentType.JSON, extension="json")


@allure.story("Создание нового бронирования")
def test_create_booking(base_URL, booking_info):
    with allure.step("Отправка запроса с данными о новом бронировании"):
        response = requests.post(url=base_URL + URL.booking_url, json=booking_info)

        with allure.step("Проверка ответа запроса"):
            assert response.status_code == 200

        with allure.step("Валидация .json ответа"):
            booking_info_schema = load_schema('post_booking.json')
            jsonschema.validate(response.json(), booking_info_schema)

    with allure.step("Получение id созданного бронирования"):
        booking_id = str(response.json()['bookingid'])

        allure.attach(body=str(booking_id), name="Booking ID", attachment_type=AttachmentType.TEXT,
                      extension="txt")

    with allure.step("Получение информации о созданном бронировании"):
        upd_response = requests.get(url=base_URL + URL.booking_url + booking_id)

        with allure.step("Проверка ответа запроса"):
            assert upd_response.status_code == 200

        with allure.step("Валидация .json ответа"):
            new_booking_info_schema = load_schema('get_booking_info.json')
            jsonschema.validate(upd_response.json(), new_booking_info_schema)

        with allure.step("Проверка соответствия информации в созданном бронировании"):
            assert booking_info == upd_response.json()

    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Created booking response",
                  attachment_type=AttachmentType.JSON, extension="json")
    allure.attach(body=json.dumps(upd_response.json(), indent=4, ensure_ascii=True),
                  name=f"Response by booking ID {booking_id}", attachment_type=AttachmentType.JSON, extension="json")

@allure.story("Удаление случайного бронирования")
def test_delete_booking(base_URL, booking_info, user_name, password):
    with allure.step("Получение токена для возможности редактирования бронирования"):
        token = get_token(base_URL, user_name, password)

    with allure.step("Получение id одного из случайных бронирований"):
        booking_id = str(get_random_booking_id(base_URL))

        response = requests.get(url=base_URL + URL.booking_url + booking_id)

        with allure.step("Проверка ответа запроса"):
            assert response.status_code == 200

        with allure.step("Валидация .json ответа"):
            booking_info_schema = load_schema('get_booking_info.json')
            jsonschema.validate(response.json(), booking_info_schema)

    delete_response = requests.delete(url=base_URL + URL.booking_url + booking_id, json=booking_info,
                                   headers={"Cookie": f"token={token}"})

    with allure.step("Проверка ответа запроса"):
        assert delete_response.status_code == 201

    allure.attach(body=str(delete_response.status_code), name="Booking delete response status code",
                  attachment_type=AttachmentType.TEXT, extension="txt")
    allure.attach(body=delete_response.content, name="Booking delete response content",
                  attachment_type=AttachmentType.TEXT, extension="txt")
