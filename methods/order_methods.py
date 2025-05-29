import requests
from urls import Endpoints

class OrderMethods:
    @staticmethod
    def create_order(token, ingredients):
        headers = {'Authorization': token} if token else {}
        data = {'ingredients': ingredients}
        response = requests.post(Endpoints.ORDERS, json=data, headers=headers)
        return response

    @staticmethod
    def get_user_orders(token):
        headers = {'Authorization': token}
        response = requests.get(Endpoints.USER_ORDERS, headers=headers)
        return response 