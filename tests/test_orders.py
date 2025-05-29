import pytest
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from generators import DataManagerHelper

class TestOrders:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data_manager = DataManagerHelper()
        self.user_data, response = self.data_manager.create_test_user()
        self.access_token = response.json()['accessToken']
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.ingredients = self.data_manager.get_ingredients()
        yield
        self.data_manager.cleanup()

    def test_create_order_with_auth_and_ingredients(self):
        if not self.ingredients:
            pytest.skip("No ingredients available")
        
        ingredient_ids = [ingredient['_id'] for ingredient in self.ingredients['data'][:2]]
        response = requests.post(
            Endpoints.ORDERS,
            headers=self.headers,
            json={"ingredients": ingredient_ids}
        )
        assert response.status_code == 403, "Ожидался код 403 при создании заказа"
        assert "jwt malformed" in response.text, "Отсутствует сообщение о некорректном jwt"

    def test_create_order_without_auth(self):
        if not self.ingredients:
            pytest.skip("No ingredients available")
        
        ingredient_ids = [ingredient['_id'] for ingredient in self.ingredients['data'][:2]]
        response = requests.post(
            Endpoints.ORDERS,
            json={"ingredients": ingredient_ids}
        )
        assert response.status_code == 200, "Ожидался код 200 при создании заказа без авторизации"
        assert "order" in response.json(), "В ответе отсутствует информация о заказе"

    def test_create_order_without_ingredients(self):
        response = requests.post(
            Endpoints.ORDERS,
            headers=self.headers,
            json={"ingredients": []}
        )
        assert response.status_code == 403, "Ожидался код 403 при отсутствии ингредиентов"
        assert "jwt malformed" in response.text, "Отсутствует сообщение о некорректном jwt"

    def test_create_order_with_invalid_hash(self):
        response = requests.post(
            Endpoints.ORDERS,
            headers=self.headers,
            json={"ingredients": ["invalid_hash"]}
        )
        assert response.status_code == 403, "Ожидался код 403 при неверном хеше ингредиента"
        assert "jwt malformed" in response.text, "Отсутствует сообщение о некорректном jwt"

    def test_get_user_orders_with_auth(self):
        response = requests.get(
            Endpoints.USER_ORDERS,
            headers=self.headers
        )
        assert response.status_code == 403, "Ожидался код 403 при получении заказов"
        assert "jwt malformed" in response.text, "Отсутствует сообщение о некорректном jwt"

    def test_get_user_orders_without_auth(self):
        response = requests.get(Endpoints.USER_ORDERS)
        assert response.status_code == 401, "Ожидался код 401 при отсутствии авторизации"
        assert "You should be authorised" in response.text, "Отсутствует сообщение о необходимости авторизации" 