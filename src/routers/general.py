from fastapi import APIRouter

from ..models.db import minesweeperIn_pydantic, minesweeper_pydantic, db_minesweeper

router = APIRouter(prefix="", tags=["General Options"])


@router.post("/join")
async def join_page(code: int):
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
