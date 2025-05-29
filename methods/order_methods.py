import requests
from urls import Endpoints

class OrderMethods:
    @staticmethod
    def create_order(access_token, ingredients):
        headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
        response = requests.post(Endpoints.ORDERS, json={'ingredients': ingredients}, headers=headers)
        return response

    @staticmethod
    def get_user_orders(access_token):
        headers = {'Authorization': f'Bearer {access_token}'} if access_token else {}
        response = requests.get(Endpoints.ORDERS, headers=headers)
        return response 