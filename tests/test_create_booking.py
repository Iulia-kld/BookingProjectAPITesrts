import pytest
import allure
import requests

from conftest import generate_random_booking_data


@allure.feature("Test Create Booking")
@allure.story("Successful booking")
def test_create_booking(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    assert response["booking"]["firstname"] == generate_random_booking_data["firstname"]
    assert response["booking"]["lastname"] == generate_random_booking_data["lastname"]
    assert response["booking"]["totalprice"] == generate_random_booking_data["totalprice"]


@allure.feature('Test Create Booking')
@allure.story('Test wrong status code')
def test_create_booking_wrong_method(api_client, generate_random_booking_data):
    with pytest.raises(requests.HTTPError):
        api_client.create_booking({})


@allure.feature('Test Create Booking')
@allure.story('Test wrong body')
def test_create_booking_missing_field(api_client, generate_random_booking_data):
    bad_date = generate_random_booking_data.copy()
    bad_date.pop("firstname")
    # response.status_code = 500
    with pytest.raises(requests.HTTPError):
        api_client.create_booking(bad_date)