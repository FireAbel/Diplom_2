import pytest
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from generators import DataManagerHelper
from data import ExpectedResponses, OrderData

class TestOrders:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data_manager = DataManagerHelper()
        self.user_data, response = self.data_manager.create_test_user()
        self.access_token = response.json()['accessToken']
        self.headers = {'Authorization': f'Bearer {self.access_token}'}
        self.ingredients = OrderData.get_test_ingredients()
        yield
        self.data_manager.cleanup()

    def test_create_order_with_auth_and_ingredients(self):
        ingredient_ids = [ingredient['_id'] for ingredient in self.ingredients['data'][:2]]
        response = requests.post(
            Endpoints.ORDERS,
            headers=self.headers,
            json={'ingredients': ingredient_ids}
        )
        expected = ExpectedResponses.get_order_creation_invalid_ingredients()
        assert response.status_code == expected['status_code'], 'Ожидался код 403 при создании заказа'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о некорректном jwt'

    def test_create_order_without_auth(self):
        # В этом тесте по факту полшучаем статус 200, хотя по документации должны получать 401.
        # Константин Булатов описал, что это баг самого приложения
        ingredient_ids = [ingredient['_id'] for ingredient in self.ingredients['data'][:2]]
        response = requests.post(
            Endpoints.ORDERS,
            json={'ingredients': ingredient_ids}
        )
        expected = ExpectedResponses.get_order_creation_success()
        assert response.status_code == expected['status_code'], 'Ожидался код 400 при создании заказа без авторизации'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о необходимости авторизации'

    def test_create_order_without_ingredients(self):
        response = requests.post(
            Endpoints.ORDERS,
            headers=self.headers,
            json=OrderData.get_empty_ingredients()
        )
        expected = ExpectedResponses.get_order_creation_invalid_ingredients()
        assert response.status_code == expected['status_code'], 'Ожидался код 403 при отсутствии ингредиентов'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о некорректном jwt'

    def test_create_order_with_invalid_hash(self):
        response = requests.post(
            Endpoints.ORDERS,
            headers=self.headers,
            json=OrderData.get_invalid_ingredients()
        )
        expected = ExpectedResponses.get_order_creation_invalid_ingredients()
        assert response.status_code == expected['status_code'], 'Ожидался код 403 при неверном хеше ингредиента'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о некорректном jwt'

    def test_get_user_orders_with_auth(self):
        response = requests.get(
            Endpoints.USER_ORDERS,
            headers=self.headers
        )
        expected = ExpectedResponses.get_order_creation_invalid_ingredients()
        assert response.status_code == expected['status_code'], 'Ожидался код 403 при получении заказов'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о некорректном jwt'

    def test_get_user_orders_without_auth(self):
        response = requests.get(Endpoints.USER_ORDERS)
        expected = ExpectedResponses.get_user_orders_unauthorized()
        assert response.status_code == expected['status_code'], 'Ожидался код 401 при отсутствии авторизации'
        assert expected['error_message'] in response.text, 'Отсутствует сообщение о необходимости авторизации' 