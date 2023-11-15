
from enum import Enum
from datetime import datetime
from bson import ObjectId


class UnsupportedFieldType(Exception):
    pass


extended_types = [ObjectId]
json_fields = [list, dict, str, int, float, bool, bytes, datetime, type(None)]


def _cast_value(value):
    if isinstance(value, Enum):
        return _cast_value(value.value)
    if type(value) not in json_fields + extended_types:
        raise UnsupportedFieldType(type(value))
    if type(value) == ObjectId:
        return value
    if type(value) == dict:
        return _cast_dict(value)
    elif type(value) == list:
        return _cast_list(value)
    elif type(value) == datetime:
        return value.isoformat()
    return value


def _cast_dict(value: dict):
    return {_cast_value(k): _cast_value(v) for k, v in value.items()}


def _cast_list(value: list):
    return [_cast_value(v) for v in value]


def get_representation(data: dict):
    return _cast_value(data)


class BaseModel:
    def get_fields(self, fields_set: str):
        fields = self.__getattribute__(fields_set)
        return {f: self.__getattribute__(f) for f in fields}

    def get_representation(self, fields_set: str):
        fields = self.get_fields(fields_set)
        return _cast_value({f: self.__getattribute__(f) for f in fields})
