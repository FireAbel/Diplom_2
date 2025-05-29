import pytest
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from generators import DataManagerHelper

class TestUserData:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data_manager = DataManagerHelper()
        self.user_data, response = self.data_manager.create_test_user()
        self.access_token = response.json()['accessToken']
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        yield
        self.data_manager.cleanup()

    def test_update_user_data_with_auth(self):
        new_name = "Updated Name"
        response = requests.patch(
            Endpoints.USER,
            headers=self.headers,
            json={"name": new_name}
        )
        assert response.status_code == 403, "Ожидался код 403 при обновлении данных"
        assert "jwt malformed" in response.text, "Отсутствует сообщение о некорректном jwt"

    def test_update_user_data_without_auth(self):
        new_name = "Updated Name"
        response = requests.patch(
            Endpoints.USER,
            json={"name": new_name}
        )
        assert response.status_code == 401, "Ожидался код 401 при отсутствии авторизации"
        assert "You should be authorised" in response.text, "Отсутствует сообщение о необходимости авторизации" 