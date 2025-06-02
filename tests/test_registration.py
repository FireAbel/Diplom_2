import pytest
import requests
import sys
import os
import allure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from data import ExpectedResponses, RegistrationData

@allure.feature('Тесты регистрации пользователя')
class TestUserRegistration:

    @pytest.fixture(autouse=True)
    def setup(self, setup_without_auth):
        pass

    @allure.title('Тест создания уникального пользователя')
    def test_create_unique_user(self):
        with allure.step('Создание нового пользователя'):
            user_data, response = self.data_manager.create_test_user()
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_registration_success()
            assert response.status_code == expected['status_code'], 'Ожидался код 200 при успешной регистрации'
            for field in expected['required_fields']:
                assert field in response.json(), f'В ответе отсутствует поле {field}'

    @allure.title('Тест создания существующего пользователя')
    def test_create_existing_user(self):
        with allure.step('Создание первого пользователя'):
            user_data, _ = self.data_manager.create_test_user()
        with allure.step('Попытка создания пользователя с теми же данными'):
            response = requests.post(Endpoints.REGISTER, json=user_data)
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_registration_user_exists()
            assert response.status_code == expected['status_code'], 'Ожидался код 403 при попытке создать существующего пользователя'
            assert expected['error_message'] in response.text, 'Отсутствует сообщение о существующем пользователе'

    @pytest.mark.parametrize("user_data,missing_field", [
        (RegistrationData.get_invalid_data_without_email(), 'email'),
        (RegistrationData.get_invalid_data_without_password(), 'password'),
        (RegistrationData.get_invalid_data_without_name(), 'name'),
    ])
    def test_create_user_without_required_field(self, user_data, missing_field):
        allure.dynamic.title(f'Тест создания пользователя без обязательного поля {missing_field}')
        with allure.step(f'Попытка создания пользователя без поля {missing_field}'):
            response = requests.post(Endpoints.REGISTER, json=user_data)
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_registration_failure()
            assert response.status_code == expected['status_code'], f'Ожидался код 403 при отсутствии обязательного поля: {missing_field}'
            assert expected['message'] in response.text, f'Отсутствует сообщение о необходимости заполнить обязательные поля при отсутствии {missing_field}'
