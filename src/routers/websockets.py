from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse

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


@router.websocket("/join/")
async def websocket_test(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        if data.size !== null
        ----> Create new game with data.size and send back the grid values
        if data.code !== null 
        ----> Join existing game and send back the grid values
        await websocket.send_text(f"Message text was: {data}")
