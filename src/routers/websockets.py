from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from ..models.db import db_minesweeper, minesweeper_pydantic

router = APIRouter(prefix="/ws", tags=["Websocket"])

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)


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
            ms = await minesweeper_pydantic.from_queryset_single(db_minesweeper.filter(code=int(data["code"])))
            ms = ms.dict()
            websocket.send_json(ms["id"])
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
