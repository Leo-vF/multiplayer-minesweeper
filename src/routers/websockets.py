from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from numpy import ravel
from typing import Dict

from ..models.db import db_minesweeper, minesweeper_pydantic, db_spot, spot_pydantic
from ..models.socketManager import WebsocketManager
from .field import open, set_Flag
from ..minesweeper import Minesweeper

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

    if str(code) not in managers.keys():
        managers.update({str("code"): WebsocketManager()})
    await managers[str(code)].connect(websocket)

    manager: WebsocketManager = managers[str(code)]

    exists = await db_spot.exists(code=code, col=0, row=0)
    if exists == True:
        field = await spot_pydantic.from_queryset(db_spot.filter(code=code))

        field = [spot.dict() for spot in field]
        await websocket.send_json({"field": field})

    else:
        ms = await minesweeper_pydantic.from_queryset_single(db_minesweeper.get(code=code))
        ms = ms.dict()
        await websocket.send_json({"n_cols": ms["n_cols"], "n_rows": ms["n_rows"]})

    try:
        while True:
            data = await websocket.receive_json()

            if data["intent"] == "open":
                data["col"] = int(data["col"])
                data["row"] = int(data["row"])

                exists = await db_spot.exists(code=code, col=data["col"], row=data["row"])
                if exists != True:
                    ms_dict = await minesweeper_pydantic.from_queryset_single(db_minesweeper.get(code=code))
                    ms_dict = ms_dict.dict()
                    ms = Minesweeper(
                        ms_dict["n_cols"],
                        ms_dict["n_rows"],
                        data["col"],
                        data["row"]
                    )
                    ms.place_mines(ms_dict["n_mines"])
                    default_values = {"opened": False,
                                      "code": ms_dict["code"], "flagged": False}
                    for spot in ravel(ms.field):
                        db_sp_obj = await db_spot.create(**{**spot.get_db_attribs(), **default_values})

                # TODO change datatype of json fields
                opened = await open(code, int(data["col"]), int(data["row"]))
                ({"opened": opened})
                await manager.broadcast({"opened": opened})

            elif data["intent"] == "flag":
                exists = await db_spot.exists(code=code, col=data["col"], row=data["row"])
                if exists != True:
                    await websocket.send_json({"error": "Can't set a flag on the first Move"})
                    continue
                # TODO change datatype of json fields
                status = set_Flag(code, int(data["col"]), int(data["row"]))
                # TODO change json depening on status
                await manager.broadcast({"flagged": status})

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # TODO send message to other clients that sb disconnected
