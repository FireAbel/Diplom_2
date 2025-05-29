import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from generators import DataManagerHelper

class TestUserLogin:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data_manager = DataManagerHelper()
        self.user_data, _ = self.data_manager.create_test_user()
        yield
        self.data_manager.cleanup()

    def test_login_with_valid_credentials(self):
        response = self.data_manager.login_test_user(
            self.user_data['email'],
            self.user_data['password']
        )
        assert response.status_code == 200, "Ожидался код 200 при успешной авторизации"
        assert "accessToken" in response.json(), "В ответе отсутствует токен доступа"

    def test_login_with_invalid_credentials(self):
        response = self.data_manager.login_test_user(
            self.user_data['email'],
            'wrong_password'
        )
        assert response.status_code == 401, "Ожидался код 401 при неверных учетных данных"
        assert "email or password are incorrect" in response.text, "Отсутствует сообщение о неверных учетных данных" 