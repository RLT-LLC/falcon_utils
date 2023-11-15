from .fields import IntegerField
from .schema import Schema


class OffsetCountSchema(Schema):
    offset = IntegerField(required=False, non_negative=True)
    count = IntegerField(required=False, non_negative=True, default=10)

    fields = ['offset', 'count']
