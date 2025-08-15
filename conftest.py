import pytest
from generators import DataManagerHelper
from data import OrderData

@pytest.fixture(autouse=True)
def setup_without_auth(request):
    data_manager = DataManagerHelper()
    request.cls.data_manager = data_manager
    yield
    data_manager.cleanup()

@pytest.fixture
def setup_with_auth(request):
    data_manager = DataManagerHelper()
    request.cls.data_manager = data_manager

    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        request.cls.user_data, register_response = data_manager.create_test_user()
        print(f"\nПопытка {attempts + 1} регистрации")
        print(f"Email: {request.cls.user_data['email']}")
        print(f"Регистрация: {register_response.status_code}")
        print(f"Ответ регистрации: {register_response.text}")
        
        if register_response.status_code == 200:
            break
        attempts += 1
        
    if register_response.status_code != 200:
        pytest.fail(f"Не удалось зарегистрировать пользователя после {max_attempts} попыток")

    login_response = data_manager.login_test_user(
        request.cls.user_data['email'],
        request.cls.user_data['password']
    )
    print(f"Авторизация: {login_response.status_code}")
    print(f"Ответ авторизации: {login_response.text}")
    
    if login_response.status_code != 200:
        pytest.fail(f"Ошибка авторизации: {login_response.status_code} - {login_response.text}")
    
    response_data = login_response.json()
    if 'accessToken' not in response_data:
        print(f"Полный ответ сервера: {response_data}")
        pytest.fail("В ответе сервера отсутствует accessToken")
        
    token = response_data['accessToken']
    token = token.replace('Bearer ', '')
    request.cls.access_token = token
    request.cls.headers = {'Authorization': f'Bearer {token}'}
    print(f"Заголовки: {request.cls.headers}")
    
    request.cls.ingredients = OrderData.get_test_ingredients()
    yield
    data_manager.cleanup() 