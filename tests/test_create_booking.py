import pytest
import allure
import requests
from pydantic.v1 import ValidationError
from conftest import generate_random_booking_data, booking_dates
from core.models.booking import BookingResponse


@allure.feature("Test Create Booking")
@allure.story("Successful booking")
def test_create_booking(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    assert response["booking"]["firstname"] == generate_random_booking_data["firstname"]
    assert response["booking"]["lastname"] == generate_random_booking_data["lastname"]
    assert response["booking"]["totalprice"] == generate_random_booking_data["totalprice"]


@allure.feature("Test Create Booking")
@allure.story("Positive: creating booking with custom data")
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Julia",
        "lastname": "Bykova",
        "totalprice": 500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-06-01",
            "checkout": "2026-06-06"
        },
        "additionalneeds": "Breakfast"
    }
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
       raise ValidationError(f"Response validation failed {e}")

    assert response["booking"]["firstname"] == booking_data["firstname"]
    assert response["booking"]["lastname"] == booking_data["lastname"]
    assert response["booking"]["totalprice"] == booking_data["totalprice"]
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]
    assert response["booking"]["additionalneeds"] == booking_data["additionalneeds"]



@allure.feature("Test Create Booking")
@allure.story("Positive: creating booking with random data")
def test_create_booking_with_random_data(api_client, booking_dates):
    booking_data = {
        "firstname": "Julia",
        "lastname": "Bykova",
        "totalprice": 500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": booking_dates["checkin"],
            "checkout": booking_dates["checkout"]
        },
        "additionalneeds": "Breakfast"
    }
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")

    assert response["booking"]["firstname"] == booking_data["firstname"]
    assert response["booking"]["lastname"] == booking_data["lastname"]
    assert response["booking"]["totalprice"] == booking_data["totalprice"]
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_dates["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_dates["checkout"]
    assert response["booking"]["additionalneeds"] == booking_data["additionalneeds"]


@allure.feature('Test Create Booking')
@allure.story('Negative: Test wrong status code')
def test_create_booking_wrong_method(api_client, generate_random_booking_data):
    with pytest.raises(requests.HTTPError):
        api_client.create_booking({})


@allure.feature('Test Create Booking')
@allure.story('Negative: Test wrong body')
def test_create_booking_missing_field(api_client, generate_random_booking_data):
    bad_date = generate_random_booking_data.copy()
    bad_date.pop("firstname")
    # response.status_code = 500
    with pytest.raises(requests.HTTPError):
        api_client.create_booking(bad_date)

@allure.feature("Test Create Booking")
@allure.story("Negative: creating booking with empty data")
def test_create_booking_with_empty_data(api_client):
    booking_data = {
        "firstname": "",
        "lastname": "",
        "totalprice": None,
        "depositpaid": None,
        "bookingdates": {
            "checkin": "",
            "checkout": ""
        },
        "additionalneeds": ""
    }
    with pytest.raises(requests.HTTPError):
        api_client.create_booking(booking_data)


@allure.feature("Test Create Booking")
@allure.story("Negative: creating booking with extra field")
def test_create_booking_with_extra_field(api_client):
    booking_data = {
        "firstname": "Nina",
        "lastname": "Li",
        "totalprice": 222,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2021-01-01",
            "checkout": "2022-01-02"
        },
        "additionalneeds": "Dinner",
        "entertainment": False
    }
    response = api_client.create_booking(booking_data)

    assert response["booking"]["firstname"] == booking_data["firstname"]
    assert response["booking"]["lastname"] == booking_data["lastname"]
    assert response["booking"]["totalprice"] == booking_data["totalprice"]
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]
    assert response["booking"]["additionalneeds"] == booking_data["additionalneeds"]
    assert "entertainment" not in response["booking"]
