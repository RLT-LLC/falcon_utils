from datetime import datetime


class SpecNone:
    def __bool__(self):
        return False


class BaseField:
    _args = []
    _kwargs = {}
    errors = []
    _is_valid = None
    validated_data = None
    errors_text = {
        "field_required": {
            "ru": "Пустое значение недопустимо",
            "en": "Value required"
        }
    }

    class Errors:
        REQUIRED_FIELD = "field_required"
        SHOULD_BE_STR = "should_be_str"
        MAX_LENGTH = "max_length"
        MIN_LENGTH = "min_length"

    def get_error_text(self, error_value):
        error = self.errors_text.get(error_value, {})
        text = error.get(self._localization, error.get('en'))
        if text is None:
            return "Could not retrieve error text message"
        else:
            return text

    def __init__(self, default=None, required=None, positive_only=None, min_value=None, max_value=None,
                 localization=None, dt_less_than_now=None, max_length=None, min_length=None, dt_greater_than_now=None,
                 non_negative=None, child=None):
        self._default = default
        self._required = required
        self._positive_only = positive_only
        self._min_value = min_value
        self._max_value = max_value
        self._localization = localization
        self._dt_less_than_now = dt_less_than_now
        self._min_length = min_length
        self._max_length = max_length
        self._dt_greater_than_now = dt_greater_than_now
        self._child = child
        self._non_negative = non_negative

    def _base_validate(self, value):
        self.errors = []
        if self._required and value is SpecNone:
            if self._default is None:
                self.errors.append(self.get_error_text(self.Errors.REQUIRED_FIELD))
                self._is_valid = False
            else:
                self._is_valid = True
                if self._default is not None:
                    value = self._default
                    self.validated_data = value
        else:
            self._is_valid = True
        return value

    def _validate(self, value):
        raise NotImplementedError

    def is_valid(self, value, localization):
        self._localization = localization
        value = self._base_validate(value)
        if self._is_valid:
            self._validate(value=value)
        return self._is_valid

    @property
    def is_required(self):
        return self._required


class IntegerField(BaseField):
    class Errors(BaseField.Errors):
        SHOULD_BE_INT = "should_be_int"
        POSITIVE_ONLY = "positive_only"
        NON_NEGATIVE_ONLY = "non_negative_only"
        MIN_VALUE = "min_value"
        MAX_VALUE = "max_value"

    errors_text = {
        Errors.REQUIRED_FIELD: {
            "ru": "Пустое значение недопустимо",
            "en": "Value required"
        },
        Errors.SHOULD_BE_INT: {
            "ru": "Поле должно быть целым числом",
            "en": "Field should be of type integer"
        },
        Errors.POSITIVE_ONLY: {
            "ru": "Поле должно содержать только положительные значения",
            "en": "Value should be positive only"
        },
        Errors.MIN_VALUE: {
            "ru": "Значение должно быть больше, чем {}",
            "en": "Value should be bigger than {}"
        },
        Errors.MAX_VALUE: {
            "ru": "Значение должно быть меньше, чем {}",
            "en": "Value should be less than {}"
        },
        Errors.NON_NEGATIVE_ONLY: {
            "ru": "Поле должно быть неотрицательным значением",
            "en": "Value should be non negative"
        }
    }

    def _validate(self, value, *args, **kwargs):
        self.errors = []
        if not isinstance(value, int):
            if not isinstance(value, str):
                self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_INT))
            else:
                try:
                    if float(value) != int(value):
                        self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_INT))
                except ValueError:
                    self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_INT))
            if self.errors:
                self._is_valid = False
                return
            value = int(value)
        if self._positive_only:
            if value <= 0:
                self.errors.append(self.get_error_text(self.Errors.POSITIVE_ONLY))
        if self._non_negative:
            if value < 0:
                self.errors.append(self.get_error_text(self.Errors.NON_NEGATIVE_ONLY))
        if self._min_value is not None:
            if value < self._min_value:
                self.errors.append(self.get_error_text(self.Errors.MIN_VALUE).format(self._min_value))
        if self._max_value is not None:
            if value > self._max_value:
                self.errors.append(self.get_error_text(self.Errors.MAX_VALUE).format(self._max_value))
        if not self.errors:
            self.validated_data = value
            self._is_valid = True
        else:
            self._is_valid = False


class FloatField(BaseField):
    class Errors(BaseField.Errors):
        SHOULD_BE_FLOAT = "should_be_FLOAT"
        POSITIVE_ONLY = "positive_only"
        NON_NEGATIVE_ONLY = "non_negative_only"
        MIN_VALUE = "min_value"
        MAX_VALUE = "max_value"

    errors_text = {
        Errors.REQUIRED_FIELD: {
            "ru": "Пустое значение недопустимо",
            "en": "Value required"
        },
        Errors.SHOULD_BE_FLOAT: {
            "ru": "Поле должно быть числом",
            "en": "Field should be of type number"
        },
        Errors.POSITIVE_ONLY: {
            "ru": "Поле должно содержать только положительные значения",
            "en": "Value should be positive only"
        },
        Errors.MIN_VALUE: {
            "ru": "Значение должно быть больше, чем {}",
            "en": "Value should be bigger than {}"
        },
        Errors.MAX_VALUE: {
            "ru": "Значение должно быть меньше, чем {}",
            "en": "Value should be less than {}"
        },
        Errors.NON_NEGATIVE_ONLY: {
            "ru": "Поле должно быть неотрицательным значением",
            "en": "Value should be non negative"
        }
    }

    def _validate(self, value, *args, **kwargs):
        self.errors = []
        if not isinstance(value, float):
            try:
                float(value)
            except ValueError:
                self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_FLOAT))
            if self.errors:
                self._is_valid = False
                return
            value = float(value)
        if self._positive_only:
            if value <= 0:
                self.errors.append(self.get_error_text(self.Errors.POSITIVE_ONLY))
        if self._non_negative:
            if value < 0:
                self.errors.append(self.get_error_text(self.Errors.NON_NEGATIVE_ONLY))
        if self._min_value is not None:
            if value < self._min_value:
                self.errors.append(self.get_error_text(self.Errors.MIN_VALUE).format(self._min_value))
        if self._max_value is not None:
            if value > self._max_value:
                self.errors.append(self.get_error_text(self.Errors.MAX_VALUE).format(self._max_value))
        if not self.errors:
            self.validated_data = value
            self._is_valid = True
        else:
            self._is_valid = False


class IsoDateTimeField(BaseField):
    class Errors(BaseField.Errors):
        SHOULD_BE_STR = "should_be_str"
        SHOULD_BE_VALID_ISO = "should_be_valid_iso"
        SHOULD_BE_PAST = "should_be_past"
        SHOULD_BE_FUTURE = "should_be_future"

    errors_text = {
        Errors.REQUIRED_FIELD: {
            "ru": "Пустое значение недопустимо",
            "en": "Value required"
        },
        Errors.SHOULD_BE_STR: {
            "ru": "Поле должно быть представлено строкой",
            "en": "Field should be of type string"
        },
        Errors.SHOULD_BE_VALID_ISO: {
            "ru": "Поле должно быть валидной строкой в ISO-формате",
            "en": "Field should be a valid ISO-format string"
        },
        Errors.SHOULD_BE_PAST: {
            "ru": "Поле должно указывать на дату в прошлом",
            "en": "Field should be datetime in the past"
        },
        Errors.SHOULD_BE_FUTURE: {
            "ru": "Поле должно указывать на дату в будущем",
            "en": "Field should be datetime in the future"
        }
    }

    def _validate(self, value, *args, **kwargs):
        self.errors = []
        try:
            value = datetime.fromisoformat(value)
            if self._dt_less_than_now and value > datetime.now():
                self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_PAST))
            if self._dt_greater_than_now and value < datetime.now():
                self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_FUTURE))
        except TypeError:
            self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_STR))
        except ValueError:
            self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_VALID_ISO))

        if not self.errors:
            self.validated_data = value
            self._is_valid = True
        else:
            self._is_valid = False


class StringField(BaseField):
    # todo min and max should be in base fields (and other errors)
    class Errors(BaseField.Errors):
        SHOULD_BE_STR = "should_be_str"
        MAX_LENGTH = "max_length"
        MIN_LENGTH = "min_length"

    errors_text = {
        Errors.REQUIRED_FIELD: {
            "ru": "Пустое значение недопустимо",
            "en": "Value required"
        },
        Errors.SHOULD_BE_STR: {
            "ru": "Поле должно быть представлено строкой",
            "en": "Field should be of type string"
        },
        Errors.MIN_LENGTH: {
            "ru": "Длинна строки должна быть не менее {} символов",
            "en": "String's length should at least {} symbols"
        },
        Errors.MAX_LENGTH: {
            "ru": "Длинна строки должна быть меньше, чем {} символов",
            "en": "String's length should be less than {} symbols"
        }
    }

    def _validate(self, value, *args, **kwargs):
        self.errors = []
        if not isinstance(value, str):
            self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_STR))
        else:
            if self._min_length is not None:
                if len(value) < self._min_length:
                    self.errors.append(self.get_error_text(self.Errors.MIN_LENGTH).format(self._min_length))
            if self._max_length is not None:
                if len(value) > self._max_length:
                    self.errors.append(self.get_error_text(self.Errors.MAX_LENGTH).format(self._max_length))

        if not self.errors:
            self.validated_data = value
            self._is_valid = True
        else:
            self._is_valid = False


class ListField(BaseField):
    class Errors(BaseField.Errors):
        MAX_LENGTH = "max_length"
        MIN_LENGTH = "min_length"

    errors_text = {
        Errors.REQUIRED_FIELD: {
            "ru": "Пустое значение недопустимо",
            "en": "Value required"
        },
        Errors.SHOULD_BE_STR: {
            "ru": "Поле должно быть представлено строкой",
            "en": "Field should be of type string"
        },
        Errors.MIN_LENGTH: {
            "ru": "Длинна списка должна быть не менее {}",
            "en": "List's length should at least {}"
        },
        Errors.MAX_LENGTH: {
            "ru": "Длинна списка должна быть меньше, чем {}",
            "en": "List's length should be less than {}"
        }
    }

    def _validate(self, value, *args, **kwargs):
        child: BaseField = self._child
        if child is None or not issubclass(type(child), BaseField):
            raise Exception('Child not passed into listfield')
        self.errors = []
        if not isinstance(value, list):
            self.errors.append(self.get_error_text(self.Errors.SHOULD_BE_STR))
        else:
            for i in range(len(value)):
                if not child.is_valid(value[i], self._localization):
                    self.errors.append(child.errors)
                    break
        if not self.errors:
            self.validated_data = value
            self._is_valid = True
        else:
            self._is_valid = False
