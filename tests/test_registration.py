import pytest
import requests
import sys
import os
import allure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from data import ExpectedResponses, RegistrationData

@allure.title("Тесты регистрации пользователя")
class TestUserRegistration:

    @pytest.fixture(autouse=True)
    def setup(self, setup_without_auth):
        pass

    @allure.step("Тест создания уникального пользователя")
    def test_create_unique_user(self):
        user_data, response = self.data_manager.create_test_user()
        expected = ExpectedResponses.get_registration_success()
        assert response.status_code == expected['status_code'], 'Ожидался код 200 при успешной регистрации'
        for field in expected['required_fields']:
            assert field in response.json(), f'В ответе отсутствует поле {field}'

    @allure.step("Тест создания существующего пользователя")
    def test_create_existing_user(self):
        user_data, _ = self.data_manager.create_test_user()
        response = requests.post(Endpoints.REGISTER, json=user_data)
        expected = ExpectedResponses.get_registration_user_exists()
        assert response.status_code == expected['status_code'], 'Ожидался код 403 при попытке создать существующего пользователя'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о существующем пользователе'

    @allure.step("Тест создания пользователя без обязательного поля")
    @pytest.mark.parametrize("user_data,missing_field", [
        (RegistrationData.get_invalid_data_without_email(), 'email'),
        (RegistrationData.get_invalid_data_without_password(), 'password'),
        (RegistrationData.get_invalid_data_without_name(), 'name'),
    ])
    def test_create_user_without_required_field(self, user_data, missing_field):
        response = requests.post(Endpoints.REGISTER, json=user_data)
        expected = ExpectedResponses.get_registration_failure()
        assert response.status_code == expected['status_code'], f'Ожидался код 403 при отсутствии обязательного поля: {missing_field}'
        assert expected['message'] in response.text, f'Отсутствует сообщение о необходимости заполнить обязательные поля при отсутствии {missing_field}'
