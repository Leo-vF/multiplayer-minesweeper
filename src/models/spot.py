from tortoise.models import Model
from tortoise import fields


class spot(Model):
    row = fields.IntField()
    col = fields.IntField()
    shown = fields.BoolField(default=False)
    bomb = fields.BoolField(default=False)
    val = fields.IntField(default=0)
