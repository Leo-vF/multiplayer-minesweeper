from fastapi import APIRouter
from numpy import ravel

from ..minesweeper import Minesweeper
from ..ms_models import db_minesweeper, db_spot, minesweeperIn_pydantic, spot_pydantic

router = APIRouter(prefix="/field",
                   tags=["Minesweeper field Operations"])


@router.post("/new/")
async def new_field(msIn: minesweeperIn_pydantic):
    msIn_dict = msIn.dict()
    ms = Minesweeper(
        msIn_dict["n_cols"],
        msIn_dict["n_rows"],
        msIn_dict["start_col"],
        msIn_dict["start_row"]
    )
    ms.place_mines(msIn_dict["n_mines"])
    msIn_dict.update({"n_mines": ms.n_mines})
    db_ms_obj = await db_minesweeper.create(**msIn_dict)
    default_values = {"opened": False, "code": msIn_dict["code"]}
    for spot in ravel(ms.field):
        db_sp_obj = await db_spot.create(**{**spot.get_db_attribs(), **default_values})
    return msIn_dict


@router.get("/{code}-{col}-{row}")
async def get_spot(code: int, col: int, row: int):
    return await spot_pydantic.from_queryset_single(
        db_spot.get(code=code, col=col, row=row))
