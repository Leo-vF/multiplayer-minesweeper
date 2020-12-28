from tortoise.models import Model
from tortoise import fields

from .spot import spot


class p_minesweeper(Model):
    id = fields.IntField(pk=True)
    code = fields.IntField()
    field = fields.foreignKeyField(spot, on_delete=fields.CASCADE)
