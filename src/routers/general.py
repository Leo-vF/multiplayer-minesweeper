from fastapi import APIRouter

router = APIRouter(prefix="", tags=["UI Endpoints"])


@router.get("/game")
def game_page():
    pass


@router.get("/join")
def join_page():
    pass


@router.get("/new_game")
def create_new_game():
    pass
