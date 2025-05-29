import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from generators import DataManagerHelper
from data import ExpectedResponses

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
        expected = ExpectedResponses.get_login_success()
        assert response.status_code == expected['status_code'], 'Ожидался код 200 при успешной авторизации'
        for field in expected['required_fields']:
            assert field in response.json(), f'В ответе отсутствует поле {field}'

    def test_login_with_invalid_credentials(self):
        response = self.data_manager.login_test_user(
            self.user_data['email'],
            'wrong_password'
        )
        expected = ExpectedResponses.get_login_invalid_credentials()
        assert response.status_code == expected['status_code'], 'Ожидался код 401 при неверных учетных данных'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о неверных учетных данных' 