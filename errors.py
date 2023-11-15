from falcon.errors import HTTPError

translations = {
    1: {
        "ru": "Непредвиденная ошибка",
        "en": "Unexpected error"
    },
    20: {
        "ru": "Ошибка валидации",
        "en": "Validation error"
    }
}

class ExceptionCodes:
    SomeException = 1
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
