from tortoise.models import Model
from tortoise import fields


class db_minesweeper(Model):
    """The Database model for a minesweeper game.

    Attributes / fields:
     - id [UUIDField] : Is the primary key for identifying a game
     - code [IntField] : The Code players need to enter to join a game
     - field [jsonField] : json representation of the entire field with mines and field values
     - open_field [jsonField] : json representation of all the fields that have been opened/marked by players
    """
    id = fields.UUIDField(pk=True)
    spots = fields.ForeignKeyField(model_name="models.db_Spot")

    #
    # code = fields.IntField(unique=True)                           # the code to enter the same game
    # field = fields.jsonField()                                    # the entire field that is saved after correct generation
    # open_field = fields.jsonField()                               # all the opened and marked fields
    #


class db_Spot(Model):
    id = fields.UUIDField(pk=True)
    col = fields.IntField()
    row = fields.IntField()
