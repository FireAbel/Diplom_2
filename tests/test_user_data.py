import pytest
import requests
import sys
import os
import allure
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from data import ExpectedResponses

@allure.feature('Тесты обновления данных пользователя')
class TestUserData:

    @pytest.fixture(autouse=True)
    def setup(self, setup_with_auth):
        pass

    @allure.title('Тест обновления данных пользователя с авторизацией')
    def test_update_user_data_with_auth(self):
        with allure.step('Подготовка данных для обновления'):
            user_data = {
                "name": "Updated Name",
                "email": f"updated_{random.randint(1000, 9999)}@example.com"
            }
        with allure.step('Обновление данных пользователя'):
            print(f"\nЗаголовки запроса: {self.headers}")
            response = requests.patch(Endpoints.USER, json=user_data, headers=self.headers)
            print(f"Ответ сервера: {response.text}")
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_user_update_success()
            assert response.status_code == expected['status_code'], 'Ожидался код 200 при обновлении данных'
            assert 'user' in response.json(), 'В ответе отсутствует информация о пользователе'

    @allure.title('Тест обновления данных пользователя без авторизации')
    @pytest.mark.usefixtures("setup_without_auth")
    def test_update_user_data_without_auth(self):
        with allure.step('Подготовка данных для обновления'):
            user_data = {
                "name": "Updated Name",
                "email": f"updated_{random.randint(1000, 9999)}@example.com"
            }
        with allure.step('Попытка обновления данных без авторизации'):
            response = requests.patch(Endpoints.USER, json=user_data)
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_user_update_failure()
            assert response.status_code == expected['status_code'], 'Ожидался код 401 при обновлении данных без авторизации' 