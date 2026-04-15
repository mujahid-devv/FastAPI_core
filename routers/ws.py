from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["Websockets"])


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client Disconnected")
