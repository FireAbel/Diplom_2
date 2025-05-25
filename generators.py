import random
import string
import requests
from data import Endpoints

class UserDataGenerator:
    @staticmethod
    def generate_login():
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        number = random.randint(100, 999)
        email = f"{username}{number}@yandex.ru"
        return email

    @staticmethod
    def generate_password():
        password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return password

    @staticmethod
    def generate_name():
        name = ''.join(random.choices(string.ascii_lowercase, k=6))
        return f"Test User {name}"

    @staticmethod
    def generate_user_data():
        return {
            "email": UserDataGenerator.generate_login(),
            "password": UserDataGenerator.generate_password(),
            "name": UserDataGenerator.generate_name()
        }

class DataManagerHelper:
    def __init__(self):
        self.base_url = "https://stellarburgers.nomoreparties.site/api"
        self.ingredients = None

    def create_test_user(self):
        email = self.generate_random_email()
        password = self.generate_random_password()
        name = self.generate_random_name()
        user_data = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f"{self.base_url}/auth/register", json=user_data)
        return user_data, response

    def login_test_user(self, email, password):
        login_data = {
            "email": email,
            "password": password
        }
        return requests.post(f"{self.base_url}/auth/login", json=login_data)

    def get_ingredients(self):
        if not self.ingredients:
            response = requests.get(f"{self.base_url}/ingredients")
            if response.status_code == 200:
                self.ingredients = response.json()
        return self.ingredients

    def cleanup(self):
        # Здесь можно добавить логику очистки тестовых данных, если необходимо
        pass

    @staticmethod
    def generate_random_email():
        return f"test_{random.randint(1000, 9999)}@example.com"

    @staticmethod
    def generate_random_password():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    @staticmethod
    def generate_random_name():
        return f"Test User {random.randint(1000, 9999)}"
