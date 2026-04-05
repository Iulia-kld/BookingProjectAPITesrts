from asyncio import timeout
from http.client import responses
from os import getenv
import requests
import os
from dotenv import load_dotenv
from dotenv.cli import unset
from core.settings.environments import Environment
import allure
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts

load_dotenv()

class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIROMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError (f"Unsupported enviroment value {environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.headers = {
            'Content=Type': 'application/json'
        }
    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported enviroment {environment}")

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
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert atatus code"):
            assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
        return response.status_code

    @allure.title("API auth check")
    def auth(self):
        with allure.step("Setting authenticate"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}"
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step("Assert atatus code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        token = response.json().get("token")
        with allure.step("Updating the header with authorization"):
           self.session.update({"Authorization": f"Bearer {token}"})

    @allure.title("Get booking by id")
    def get_booking_by_id(self, id):
        with allure.step("Setting booking"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{id}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert atatus code"):
            assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
        return response.json()