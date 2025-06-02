import requests
from urls import Endpoints

class IngredientMethods:
    @staticmethod
    def get_ingredients():
        response = requests.get(Endpoints.BASE_URL + '/ingredients')
        return response

    @staticmethod
    def get_ingredient_by_id(ingredient_id):
        response = requests.get(f"{Endpoints.BASE_URL}/ingredients/{ingredient_id}")
        return response

    @staticmethod
    def get_valid_ingredients():
        response = requests.get(Endpoints.BASE_URL + '/ingredients')
        if response.status_code == 200:
            ingredients = response.json()['data']
            return [ingredient['_id'] for ingredient in ingredients[:3]]
        return [] 