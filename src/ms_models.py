from tortoise.fields.base import CASCADE
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class db_minesweeper(Model):
    """The Database model for a minesweeper game.

    Attributes / fields:
     - id [UUIDField] : Is the primary key for identifying a game.
     - spots [ForeignKeyField] : Foreign Key to all Spots of the minesweeper field.
     - code [IntField] : The Code players need to enter to join a game.
     - n_cols [SmallIntField]: The number of columns
     - n_rows [SmallIntField]: The number of rows
    """
    id = fields.UUIDField(pk=True)      # the code to enter the same game
    spots = fields.ForeignKeyField(
        model_name="models.db_spot", on_delete=CASCADE)    # the entire field of spots
    code = fields.SmallIntField(unique=True)
    n_cols = fields.SmallIntField()
    n_rows = fields.SmallIntField()


class db_spot(Model):
    """The database model for a single spot of a minesweeper board. Each Spot is tied to a single board with the foreignKey field of db_minesweeper.

    Args:
        id [UUIDField]: The primary key for each spot.
        col [SmallIntField]: Holds the column of the spot in its minesweeper board. 16bit signed integer.
        row [SmallIntField]: Holds the row of the spot in its minesweeper board. 16bit signed integer.
        opened [BooleanField]: True if the players already opened the spot or not.
        mine [BooleanField]: True if the spot contains a mine false if it does not.
        n_mines [SmallIntField]: Contains the number of neighboring mines. 16bit signed integer.
    """
    id = fields.UUIDField(pk=True)
    col = fields.SmallIntField()
    row = fields.SmallIntField()
    openend = fields.BooleanField()
    mine = fields.BooleanField()
    n_mines = fields.SmallIntField()


minesweeper_pydantic = pydantic_model_creator(
    db_minesweeper, name="minesweeper_pydantic")
minesweeperIn_pydantic = pydantic_model_creator(
    db_minesweeper, name="minesweeperIn_pydantic", exclude=("id"))
spot_pydantic = pydantic_model_creator(db_spot, name="spot_pydantic")
