from fastapi import Router

router = Router(prefix="/field", tags="Minesweeper field Operations")


@router.get("/{row}-{col}")
def get_spot(row: int, col: int):
    pass
