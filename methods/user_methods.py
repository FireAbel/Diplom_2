import requests
from urls import Endpoints
from generators import UserDataGenerator

class UserMethods:
    @staticmethod
    def register_user():
        user_data = UserDataGenerator.generate_user_data()
        response = requests.post(Endpoints.REGISTER, json=user_data)
        return response, user_data

    @staticmethod
    def login_user(email, password):
        login_data = {
            "email": email,
            "password": password
        }
        response = requests.post(Endpoints.LOGIN, json=login_data)
        return response

    @staticmethod
    def update_user_data(access_token, user_data):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.patch(Endpoints.USER, json=user_data, headers=headers)
        return response

    @staticmethod
    def delete_user(token):
        headers = {'Authorization': token}
        response = requests.delete(Endpoints.USER, headers=headers)
        return response 