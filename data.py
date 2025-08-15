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
    def get_invalid_data_without_email():
        return {
            'password': 'test_password',
            'name': 'Test User'
        }

    @staticmethod
    def get_invalid_data_without_password():
        return {
            'email': 'test@example.com',
            'name': 'Test User'
        }

    @staticmethod
    def get_invalid_data_without_name():
        return {
            'email': 'test@example.com',
            'password': 'test_password'
        }

# Тестовые данные для заказов
class OrderData:
    @staticmethod
    def get_empty_ingredients():
        return {'ingredients': []}

    @staticmethod
    def get_invalid_ingredients():
        return {'ingredients': ['invalid_hash']}

    @staticmethod
    def get_test_ingredients():
        return {
            'data': [
                {
                    '_id': '61c0c5a71d1f82001bdaaa6c',
                    'name': 'Краторная булка N-200i'
                },
                {
                    '_id': '61c0c5a71d1f82001bdaaa71',
                    'name': 'Биокотлета из марсианской Магнолии'
                }
            ]
        }

# Ожидаемые ответы для тестов
class ExpectedResponses:
    @staticmethod
    def get_registration_success():
        return {
            'status_code': 200,
            'message': 'User successfully registered',
            'required_fields': ['accessToken', 'user']
        }

    @staticmethod
    def get_registration_failure():
        return {
            'status_code': 403,
            'message': ErrorMessages.REQUIRED_FIELDS
        }

    @staticmethod
    def get_registration_user_exists():
        return {
            'status_code': 403,
            'error_message': ErrorMessages.USER_EXISTS
        }

    @staticmethod
    def get_login_success():
        return {
            'status_code': 200,
            'message': 'User successfully logged in',
            'required_fields': ['accessToken', 'user']
        }

    @staticmethod
    def get_login_failure():
        return {
            'status_code': 401,
            'message': ErrorMessages.INVALID_CREDENTIALS
        }

    @staticmethod
    def get_login_invalid_credentials():
        return {
            'status_code': 401,
            'error_message': ErrorMessages.INVALID_CREDENTIALS
        }

    @staticmethod
    def get_order_creation_success():
        return {
            'status_code': 200,
            'message': 'Order created successfully'
        }

    @staticmethod
    def get_order_creation_failure():
        return {
            'status_code': 400,
            'message': 'Invalid order data'
        }

    @staticmethod
    def get_user_orders_success():
        return {
            'status_code': 200,
            'message': 'User orders retrieved successfully'
        }

    @staticmethod
    def get_user_orders_failure():
        return {
            'status_code': 401,
            'message': 'User not authorized'
        }

    @staticmethod
    def get_user_update_success():
        return {
            'status_code': 200,
            'message': 'User data updated successfully'
        }

    @staticmethod
    def get_user_update_failure():
        return {
            'status_code': 401,
            'message': 'User not authorized'
        } 