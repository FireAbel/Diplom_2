"""
Модуль с тестовыми данными и ожидаемыми ответами для API тестов.
"""

# Ожидаемые коды ответов
class StatusCodes:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404

# Ожидаемые сообщения об ошибках
class ErrorMessages:
    USER_EXISTS = 'User already exists'
    REQUIRED_FIELDS = 'Email, password and name are required fields'
    INVALID_CREDENTIALS = 'email or password are incorrect'
    JWT_MALFORMED = 'jwt malformed'
    UNAUTHORIZED = 'You should be authorised'

# Ожидаемые поля в ответах
class ResponseFields:
    ACCESS_TOKEN = 'accessToken'
    ORDER = 'order'

# Тестовые данные для регистрации
class RegistrationData:
    @staticmethod
    def get_invalid_data():
        return {
            'password': 'test_password',
            'name': 'Test User'
        }

# Тестовые данные для заказов
class OrderData:
    @staticmethod
    def get_empty_ingredients():
        return {'ingredients': []}

    @staticmethod
    def get_invalid_ingredients():
        return {'ingredients': ['invalid_hash']}

# Ожидаемые ответы для тестов
class ExpectedResponses:
    @staticmethod
    def get_registration_success():
        return {
            'status_code': StatusCodes.OK,
            'required_fields': [ResponseFields.ACCESS_TOKEN]
        }

    @staticmethod
    def get_registration_user_exists():
        return {
            'status_code': StatusCodes.FORBIDDEN,
            'error_message': ErrorMessages.USER_EXISTS
        }

    @staticmethod
    def get_registration_missing_fields():
        return {
            'status_code': StatusCodes.FORBIDDEN,
            'error_message': ErrorMessages.REQUIRED_FIELDS
        }

    @staticmethod
    def get_login_success():
        return {
            'status_code': StatusCodes.OK,
            'required_fields': [ResponseFields.ACCESS_TOKEN]
        }

    @staticmethod
    def get_login_invalid_credentials():
        return {
            'status_code': StatusCodes.UNAUTHORIZED,
            'error_message': ErrorMessages.INVALID_CREDENTIALS
        }

    @staticmethod
    def get_order_creation_success():
        return {
            'status_code': StatusCodes.OK,
            'required_fields': [ResponseFields.ORDER]
        }

    @staticmethod
    def get_order_creation_unauthorized():
        return {
            'status_code': StatusCodes.UNAUTHORIZED,
            'error_message': ErrorMessages.UNAUTHORIZED
        }

    @staticmethod
    def get_order_creation_invalid_ingredients():
        return {
            'status_code': StatusCodes.FORBIDDEN,
            'error_message': ErrorMessages.JWT_MALFORMED
        }

    @staticmethod
    def get_user_orders_unauthorized():
        return {
            'status_code': StatusCodes.UNAUTHORIZED,
            'error_message': ErrorMessages.UNAUTHORIZED
        } 