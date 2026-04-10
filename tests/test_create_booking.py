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
def test_create_booking_wrong_method(api_client, mocker, generate_random_booking_data):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status code 200 but got 405"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature('Test Create Booking')
@allure.story('Test wrong URL')
def test_create_booking_not_found(api_client, mocker, generate_random_booking_data):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status code 200 but got 404"):
        api_client.create_booking(generate_random_booking_data)