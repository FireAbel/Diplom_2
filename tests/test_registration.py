import pytest
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from generators import DataManagerHelper
from data import ExpectedResponses, RegistrationData

class TestUserRegistration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data_manager = DataManagerHelper()
        yield
        self.data_manager.cleanup()

    def test_create_unique_user(self):
        user_data, response = self.data_manager.create_test_user()
        expected = ExpectedResponses.get_registration_success()
        assert response.status_code == expected['status_code'], 'Ожидался код 200 при успешной регистрации'
        for field in expected['required_fields']:
            assert field in response.json(), f'В ответе отсутствует поле {field}'

    def test_create_existing_user(self):
        user_data, _ = self.data_manager.create_test_user()
        response = requests.post(Endpoints.REGISTER, json=user_data)
        expected = ExpectedResponses.get_registration_user_exists()
        assert response.status_code == expected['status_code'], 'Ожидался код 403 при попытке создать существующего пользователя'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о существующем пользователе'

    def test_create_user_without_required_field(self):
        user_data = RegistrationData.get_invalid_data()
        response = requests.post(Endpoints.REGISTER, json=user_data)
        expected = ExpectedResponses.get_registration_missing_fields()
        assert response.status_code == expected['status_code'], 'Ожидался код 403 при отсутствии обязательного поля'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о необходимости заполнить обязательные поля' 