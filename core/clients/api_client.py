import requests
import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import allure
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
from core.settings.environments import Environment

load_dotenv()

class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError (f"Unsupported enviroment value: {environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json'
        }
    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported enviroment: {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    @allure.title("API ping check")
    def ping(self):
        with allure.step("Ping API client"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT.value}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert atatus code"):
            assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
        return response.status_code

    @allure.title("API auth check")
    def auth(self):
        with allure.step("Setting authenticate"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT.value}"
            payload = {"username": Users.USERNAME.value, "password": Users.PASSWORD.value}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()
        with allure.step("Assert atatus code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        token = response.json().get("token")
        with allure.step("Updating the header with authorization"):
           self.session.headers.update({"Authorization": f"Bearer {token}"})

    @allure.title("Get booking by id")
    def get_booking_by_id(self, id):
        with allure.step("Setting booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{id}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert atatus code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()

    @allure.title("Deleting booking")
    def delete_booking(self, booking_id):
        with allure.step("Deleting booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value))
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
        return response.status_code == 201


    def create_booking(self, booking_data):
        with allure.step("Creating booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})
            response = self.session.post(url, json=booking_data)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()

    def get_booking_ids(self, params=None):
        with allure.step("Getting object with booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()

    @allure.title("Update booking")
    def update_booking(self, booking_id, booking_data):
        with allure.step("Updating booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.put(url, booking_data, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value))
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()

    @allure.title("Partial update booking")
    def partial_update_booking(self, booking_id, booking_data):
        with allure.step("Partial updating booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT.value}/{booking_id}"
            response = self.session.patch(url, booking_data, auth=HTTPBasicAuth(Users.USERNAME.value, Users.PASSWORD.value))
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()
