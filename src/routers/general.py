from fastapi import APIRouter

from ..models.db import minesweeperIn_pydantic, db_minesweeper
from ..models.pydantic_models import join_pyd

router = APIRouter(prefix="", tags=["General Options"])


@router.post("/join")
async def join_page(code: join_pyd):
    """The join backend route to check whether or not the game identified by the code the user enters exists

    Args:
        code (join_pyd): The code as Pydantic Model for type validation

    Returns:
        dict: "exists": bool whether or not the game exists
    """
    code = code.dict()
    field_exists = await db_minesweeper.exists(code=code)
    return {"exists": field_exists}


@router.post("/create")
async def create_new_game(msIn: minesweeperIn_pydantic):
    msIn = msIn.dict()

    if msIn["n_cols"] <= 5:
        return {"error": "Number of colums is too small"}
    elif msIn["n_cols"] > 60:
        return {"error": "Number of columns must be at or below 60"}
    elif msIn["n_rows"] <= 5:
        return {"error": "Number of rows is too small"}
    elif msIn["n_rows"] > 60:
        return {"error": "Number of rows must be at or below 60"}
    elif msIn["n_mines"] < 1:
        return {"error": "Number of mines too small"}
    elif msIn["n_mines"] >= msIn["n_rows"]*msIn["n_cols"] - 9:
        return {"error": "Number of mines too big"}
    else:
        await db_minesweeper.create(**msIn)
        return {"success": "Game successfully created"}
