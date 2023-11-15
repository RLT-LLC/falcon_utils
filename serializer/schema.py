from copy import deepcopy
from .fields import BaseField, SpecNone
from ..errors import CustomHTTPError, ExceptionCodes


class Schema:
    data = {}
    errors = {}
    fields = []
    validated_data = {}
    _is_valid = None

    def __init__(self, data: dict):
        self.validated_data = {}
        self.errors = {}
        self.data = data
        for field in self.fields:
            _field = self.__getattribute__(field)
            self.__setattr__(field, deepcopy(_field))

    def is_valid(self, raise_exc=False, localization=None):
        self._is_valid = True
        for f in self.fields:
            field: BaseField = getattr(self, f)
            if not issubclass(field.__class__, BaseField):
                raise Exception
            value = self.data.get(f, SpecNone)
            if value is SpecNone:
                _value = field._base_validate(value)
                if _value is SpecNone:
                    continue
                self.validated_data[f] = field.validated_data
            elif field.is_valid(value, localization):
                self.validated_data[f] = field.validated_data
            else:
                self.errors[f] = field.errors
        if self.errors:
            self._is_valid = False
            if raise_exc:
                raise CustomHTTPError(ExceptionCodes.ValidationError, self.errors)
        return self._is_valid
