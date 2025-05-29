import requests
from urls import Endpoints
from generators import generate_user_data

class UserMethods:
    @staticmethod
    def register_user():
        user_data = generate_user_data()
        response = requests.post(Endpoints.REGISTER, json=user_data)
        return response, user_data

    @staticmethod
    def login_user(email, password):
        credentials = {
            "email": email,
            "password": password
        }
        response = requests.post(Endpoints.LOGIN, json=credentials)
        return response

    @staticmethod
    def update_user_data(token, new_data):
        headers = {'Authorization': token}
        response = requests.patch(Endpoints.USER, json=new_data, headers=headers)
        return response

    @staticmethod
    def delete_user(token):
        headers = {'Authorization': token}
        response = requests.delete(Endpoints.USER, headers=headers)
        return response 