import requests
from urls import Endpoints

class IngredientMethods:
    @staticmethod
    def get_ingredients():
        response = requests.get(Endpoints.BASE_URL + '/ingredients')
        return response

    @staticmethod
    def get_valid_ingredients():
        response = requests.get(Endpoints.BASE_URL + '/ingredients')
        if response.status_code == 200:
            ingredients = response.json()['data']
            # Возвращаем первые три ингредиента для тестов
            return [ingredient['_id'] for ingredient in ingredients[:3]]
        return [] 