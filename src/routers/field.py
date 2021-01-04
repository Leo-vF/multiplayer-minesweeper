from fastapi import APIRouter
from numpy import ravel
from typing import List

from numpy.core.fromnumeric import size

from ..minesweeper import Minesweeper
from ..ms_models import db_minesweeper, db_spot, minesweeperIn_pydantic, spot_pydantic, minesweeper_pydantic

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


@router.get("/open/{code}-{col}-{row}")
async def open(code: int, col: int, row: int, double_click: bool = False):
    """Get request that returns a list of squares that are opened by opening one specific one. For example a spot with 0 mines near it causes the fields around it to be opened.

    Args:
        code (int): The Code for the game the square belongs to
        col (int): The column the spot has in the game determined by code
        row (int): The row the spot has in the game determined by code
        double_click (bool): Double click to open additional fields
    """
    OPENED = []

    async def update_opened(code: int, col: int, row: int):
        await db_spot.filter(code=code, col=col, row=row).update(opened=True)

    async def open_zeros(spot: dict, code: int, size: tuple):
        """Recursive function that open's all the zero's neighbors and their neighbors if they are zero.

        Args:
            spot (dict): The dictionary of a spot_pydantic model
            code (int): The game the spot belongs to

        Returns:
            list[dict]: A list of all the spots that are opened
        """
        col, row = spot["col"], spot["row"]
        n_cols, n_rows = size

        # HACK print(f"öffne-{col}-{row}")
        if spot["n_mines"] != 0:
            await update_opened(code=code, col=col, row=row)

            OPENED.append(spot)

        else:
            neighbors = [
                (col-1, row-1), (col, row-1), (col+1, row-1),
                (col-1, row),                 (col+1, row),
                (col-1, row+1), (col, row+1), (col+1, row+1)
            ]

            if spot["opened"] == False:
                await update_opened(code, col, row)
                OPENED.append(spot)
                for nb in neighbors:
                    if 0 <= nb[0] < n_rows and 0 <= nb[1] < n_cols:
                        nb = await spot_pydantic.from_queryset_single(db_spot.get(code=code, col=nb[0], row=nb[1]))
                        nb = nb.dict()
                        if nb["opened"] == False:
                            await open_zeros(nb, code, size)

    spot = await spot_pydantic.from_queryset_single(
        db_spot.get(code=code, col=col, row=row))
    spot_dict = spot.dict()

    if spot_dict["mine"] == True:
        # TODO define better return value for frontend
        return {"game_status": "lost"}

    ms = await minesweeper_pydantic.from_queryset_single(db_minesweeper.get(code=code))
    ms = ms.dict()
    size = (ms["n_cols"], ms["n_rows"])

    # TODO make sure to open only if it is a double click or the field is not yet opened
    if not double_click:
        await open_zeros(spot_dict, code, size)
        return OPENED
