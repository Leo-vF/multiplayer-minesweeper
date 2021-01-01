from fastapi import APIRouter
from ..minesweeper import Minesweeper

router = APIRouter(prefix="/field-{code}",
                   tags=["Minesweeper field Operations"])


@router.post("/new-{n_cols}-{n_rows}")
def new_field(n_cols: int, n_rows: int, code: int):
    ms = Minesweeper(n_cols, n_rows)
    return {"code": code}


@router.get("/{col}-{row}")
def get_spot(col: int, row: int):
    pass
