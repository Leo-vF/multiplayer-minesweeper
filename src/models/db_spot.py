from tortoise.models import Model
from tortoise import fields


class db_Spot(Model):
    id = fields.UUIDField(pk=True)
    col = fields.IntField()
    row = fields.IntField()
