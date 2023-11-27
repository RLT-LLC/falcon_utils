from __future__ import annotations
import typing

from falcon_utils.base_models.base_model import get_representation

if typing.TYPE_CHECKING:
    from common.mongo import MongoWorker


class BaseResource(object):
    mongo = None
    permissions = []
    require_auth = False

    def __init__(self, mongo_manager: MongoWorker = None):
        self.mongo = mongo_manager


class APIResponse:
    @classmethod
    def OK(cls, data=None):
        if data is None:
            data = {}

        return {
            'status': 'OK',
            'data': get_representation(data),
            'message': "",
            'code': 0
        }

    @classmethod
    def ERR(cls, data=None, description="", add_msg="", code=0):
        if data is None:
            data = {}

        return {
            'status': 'ERR',
            'data': get_representation(data),
            'description': description,
            'add_msg': add_msg,
            'code': code
        }
