from fastapi import APIRouter, WebSocket

router = APIRouter(prefix="/ws", tags=["Websocket"])


@router.websocket("/")
async def websocket_test(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
