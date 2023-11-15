from falcon.errors import HTTPError

"""При добавлении новой ошибки нужно добавлять текст ошибки в translations"""
translations = {
    1: {
        "ru": "Непредвиденная ошибка",
        "en": "Unexpected error"
    },
    10: {
        "ru": "Токен не найден",
        "en": "Token not found"
    },
    20: {
        "ru": "Ошибка валидации",
        "en": "Validation Error"
    },
}

"""При добавлении новой ошибки нужно добавлять код ошибки в ExceptionCodes"""


class ExceptionCodes:
    SomeException = 1
    TokenNotFound = 10
    ValidationError = 20


class CustomHTTPError(HTTPError):
    """Represents a generic HTTP error.
    """
    code: int = 0
    text: str = ''
    data: dict
    translations: dict[int, dict[str, str]] = translations

    def __init__(self, code, data=None, localization='en', **kwargs):
        if data is None:
            data = {}

        super(CustomHTTPError, self).__init__('200')
        self.code = code
        self.data = data

    def to_dict(self, obj_type=dict, localization='en'):
        """Returns a basic dictionary representing the error."""
        return {
            'status': 'ERR',
            'data': self.data,
            'code': self.code,
            'message': self.translations[self.code].get(localization,
                                                        self.translations[self.code].get('en')),
        }
