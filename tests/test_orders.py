import pytest
import requests
import sys
import os
import allure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urls import Endpoints
from data import ExpectedResponses, OrderData

@allure.feature("Тесты заказов")
class TestOrders:

    @pytest.fixture(autouse=True)
    def setup(self, setup_with_auth):
        pass

    @pytest.fixture
    def setup_without_auth(self, request):
        request.cls.ingredients = OrderData.get_test_ingredients()

    @allure.title("Тест создания заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self):
        with allure.step('Подготовка данных для заказа'):
            ingredient_ids = [ingredient['_id'] for ingredient in self.ingredients['data'][:2]]
        with allure.step('Создание заказа'):
            response = requests.post(
                Endpoints.ORDERS,
                json={'ingredients': ingredient_ids},
                headers=self.headers
            )
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_order_creation_success()
            assert response.status_code == expected['status_code'], 'Ожидался код 200 при создании заказа'
            assert 'order' in response.json(), 'В ответе отсутствует информация о заказе'

    @allure.title("Тест создания заказа без авторизации")
    @pytest.mark.usefixtures("setup_without_auth")
    def test_create_order_without_auth(self):
        with allure.step('Подготовка данных для заказа'):
            ingredient_ids = [ingredient['_id'] for ingredient in self.ingredients['data'][:2]]
        with allure.step('Создание заказа без авторизации'):
            response = requests.post(
                Endpoints.ORDERS,
                json={'ingredients': ingredient_ids}
            )
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_user_orders_failure()
            assert response.status_code == expected['status_code'], 'Ожидался код 401 при создании заказа без авторизации'
            assert expected['message'] in response.text, 'Отсутствует сообщение о необходимости авторизации'

    @allure.title("Тест создания заказа без ингредиентов")
    def test_create_order_without_ingredients(self):
        with allure.step('Создание заказа без ингредиентов'):
            response = requests.post(
                Endpoints.ORDERS,
                json={'ingredients': []},
                headers=self.headers
            )
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_order_creation_failure()
            assert response.status_code == expected['status_code'], 'Ожидался код 400 при создании заказа без ингредиентов'

    @allure.title("Тест создания заказа с невалидным хешем ингредиента")
    def test_create_order_with_invalid_hash(self):
        with allure.step('Создание заказа с невалидным хешем'):
            response = requests.post(
                Endpoints.ORDERS,
                json={'ingredients': ['invalid_hash']},
                headers=self.headers
            )
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_order_creation_failure()
            assert response.status_code == expected['status_code'], 'Ожидался код 400 при создании заказа с невалидным хешем'

    @allure.title("Тест получения заказов пользователя с авторизацией")
    def test_get_user_orders_with_auth(self):
        with allure.step('Получение заказов пользователя'):
            response = requests.get(Endpoints.ORDERS, headers=self.headers)
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_user_orders_success()
            assert response.status_code == expected['status_code'], 'Ожидался код 200 при получении заказов'
            assert 'orders' in response.json(), 'В ответе отсутствует список заказов'

    @allure.title("Тест получения заказов пользователя без авторизации")
    def test_get_user_orders_without_auth(self):
        with allure.step('Получение заказов без авторизации'):
            response = requests.get(Endpoints.ORDERS)
        with allure.step('Проверка ответа сервера'):
            expected = ExpectedResponses.get_user_orders_failure()
            assert response.status_code == expected['status_code'], 'Ожидался код 401 при получении заказов без авторизации' 