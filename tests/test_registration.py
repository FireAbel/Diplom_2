import pytest
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from generators import DataManagerHelper

class TestUserRegistration:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data_manager = DataManagerHelper()
        yield
        self.data_manager.cleanup()

    def test_create_unique_user(self):
        user_data, response = self.data_manager.create_test_user()
        assert response.status_code == 200, "Ожидался код 200 при успешной регистрации"
        assert "accessToken" in response.json(), "В ответе отсутствует токен доступа"

    def test_create_existing_user(self):
        user_data, _ = self.data_manager.create_test_user()
        response = requests.post(Endpoints.REGISTER, json=user_data)
        assert response.status_code == 403, "Ожидался код 403 при попытке создать существующего пользователя"
        assert "User already exists" in response.text, "Отсутствует сообщение о существующем пользователе"

    def test_create_user_without_required_field(self):
        user_data = self.data_manager.create_test_user()[0]
        del user_data['email']
        response = requests.post(Endpoints.REGISTER, json=user_data)
        assert response.status_code == 403, "Ожидался код 403 при отсутствии обязательного поля"
        assert "Email, password and name are required fields" in response.text, "Отсутствует сообщение о необходимости заполнить обязательные поля" 