from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from typing import Dict

from ..models.db import db_minesweeper, minesweeper_pydantic, db_spot, spot_pydantic
from ..models.socketManager import WebsocketManager
from .field import open, set_Flag

router = APIRouter(prefix="/ws", tags=["Websocket"])

managers: Dict[str, WebsocketManager] = {}


@router.websocket("/create")
async def ws_create(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()

    if int(data["n_cols"]) <= 3:
        await websocket.send_json({"error": "Number of colums is too small"})
    elif int(data["n_cols"]) > 60:
        await websocket.send_json({"error": "Number of columns must be at or below 60"})
    elif int(data["n_rows"]) <= 3:
        await websocket.send_json({"error": "Number of rows is too small"})
    elif int(data["n_rows"]) > 60:
        await websocket.send_json({"error": "Number of rows must be at or below 60"})
    elif int(data["n_mines"]) < 1:
        await websocket.send_json({"error": "Number of mines too small"})
    elif int(data["n_mines"]) >= int(data["n_rows"])*int(data["n_cols"]):
        await websocket.send_json({"error": "Number of mines too big"})
    else:
        try:
            await db_minesweeper.create(**data)
            ms = await minesweeper_pydantic.from_queryset_single(db_minesweeper.get(code=int(data["code"])))
            ms = ms.dict()

            managers.update({str(data["code"]): WebsocketManager()})

            await websocket.send_json({"succes": "Game succesfully created"})
        except Exception as e:
            await websocket.send_text(str(e))


@router.websocket("/join")
async def ws_join(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()
    try:
        db_minesweeper.filter(code=data["code"])
    except Exception as e:
        await websocket.send_text(str(e))


@router.websocket("/game/{code}")
async def ws_open(websocket: WebSocket, code: int):
    """The Websocket that is used for the entire game, to allow broadcasting one players actions to the other participants.

    Args:
        websocket (WebSocket): The Websocket used for the connection
        code (int): The Code that uniquely identifies a single game
    """

    await managers[str(code)].connect(websocket)
    manager: WebsocketManager = managers[str(code)]

    try:
        field = await spot_pydantic.from_queryset(db_spot.get(code=code))

        field = [spot.dict() for spot in field]
        websocket.send_json({"field": field})
    except:
        ms = await minesweeper_pydantic.from_queryset_single(db_minesweeper.get(code=code))
        websocket.send_json({"n_cols": ms["n_cols"], "n_rows": ms["n_rows"]})
    try:
        while True:
            data = await websocket.receive_json()

            if data["intent"] == "open":
                # TODO change datatype of json fields
                opened = await open(code, int(data["col"]), int(data["row"]))
                ({"opened": opened})
                manager.broadcast({"opened": opened})

            elif data["intent"] == "flag":
                # TODO change datatype of json fields
                status = set_Flag(code, int(data["col"]), int(data["row"]))
                # TODO change json depening on status
                manager.broadcast({"flagged": status})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # TODO send message to other clients that sb disconnected
