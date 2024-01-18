import json
import logging
import allure
import requests
from allure_commons.types import AttachmentType

token_url = 'auth/'
booking_url = 'booking/'

def get_booikngs(base_url):
    response = requests.get(url=base_url + booking_url)
    allure.attach(body=response.request.url, name="Request URL", attachment_type=AttachmentType.TEXT)
    allure.attach(body=response.request.method, name="Request method", attachment_type=AttachmentType.TEXT)
    allure.attach(body=str(response.status_code), name="Response status code", attachment_type=AttachmentType.TEXT,
                  extension='txt')
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response body",
                  attachment_type=AttachmentType.JSON, extension="json")
    logging.info("Request: " + response.request.url)
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)
    return response

def get_booikng_info(base_url, booking_id):
    response = requests.get(url=base_url + booking_url + booking_id)
    allure.attach(body=response.request.url, name="Request URL", attachment_type=AttachmentType.TEXT)
    allure.attach(body=response.request.method, name="Request method", attachment_type=AttachmentType.TEXT)
    allure.attach(body=str(response.status_code), name="Response status code", attachment_type=AttachmentType.TEXT,
                  extension='txt')
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response body",
                  attachment_type=AttachmentType.JSON, extension="json")
    logging.info("Request: " + response.request.url)
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)
    return response

def update_booikng(base_url, booking_id, booking_info, token):
    response = requests.put(url=base_url + booking_url + booking_id, json=booking_info,
                            headers={"Cookie": f"token={token}"})
    allure.attach(body=response.request.url, name="Request URL", attachment_type=AttachmentType.TEXT)
    allure.attach(body=response.request.method, name="Request method", attachment_type=AttachmentType.TEXT)
    allure.attach(body=str(response.status_code), name="Response status code", attachment_type=AttachmentType.TEXT,
                  extension='txt')
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response body",
                  attachment_type=AttachmentType.JSON, extension="json")
    logging.info("Request: " + response.request.url)
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)
    return response

def create_booking(base_url, booking_info):
    response = requests.post(url=base_url + booking_url, json=booking_info)
    allure.attach(body=response.request.url, name="Request URL", attachment_type=AttachmentType.TEXT)
    allure.attach(body=response.request.method, name="Request method", attachment_type=AttachmentType.TEXT)
    allure.attach(body=str(response.status_code), name="Response status code", attachment_type=AttachmentType.TEXT,
                  extension='txt')
    allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response body",
                  attachment_type=AttachmentType.JSON, extension="json")
    logging.info("Request: " + response.request.url)
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)
    return response

def delete_booking(base_url, booking_id, token):
    response = requests.delete(url=base_url + booking_url + booking_id,
                                      headers={"Cookie": f"token={token}"})
    allure.attach(body=response.request.url, name="Request URL", attachment_type=AttachmentType.TEXT)
    allure.attach(body=response.request.method, name="Request method", attachment_type=AttachmentType.TEXT)
    allure.attach(body=str(response.status_code), name="Response status code", attachment_type=AttachmentType.TEXT,
                  extension='txt')
    logging.info("Request: " + response.request.url)
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)
    return response