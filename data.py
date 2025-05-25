class Endpoints:
    BASE_URL = "https://stellarburgers.nomoreparties.site/api"
    
    # Эндпоинты для работы с пользователем
    REGISTER = f"{BASE_URL}/auth/register"  # POST - регистрация пользователя
    LOGIN = f"{BASE_URL}/auth/login"        # POST - авторизация пользователя
    USER = f"{BASE_URL}/auth/user"          # GET/PATCH - получение/изменение данных пользователя
    LOGOUT = f"{BASE_URL}/auth/logout"      # POST - выход из системы
    
    # Эндпоинты для работы с заказами
    ORDERS = f"{BASE_URL}/orders"           # POST - создание заказа
    USER_ORDERS = f"{BASE_URL}/orders"      # GET - получение заказов пользователя
    
    # Эндпоинты для работы с ингредиентами
    INGREDIENTS = f"{BASE_URL}/ingredients" # GET - получение списка ингредиентов 