from fastapi import WebSocket, Request
from starlette.websockets import WebSocketState
from manager import WSManager
from main import app


@app.websocket("/ws/{room_name}/{user_name}")
async def websocket_endpoint(websocket: WebSocket, room_name:str, user_name:str):

    try:
        # add user
        await WSManager.connect(websocket, room_name, user_name)

        while True:

            if websocket.application_state == WebSocketState.CONNECTED:
                data = await websocket.receive_text()

                await WSManager.broadcast(f"data", room_name, user_name)
    
    except Exception as ex:
        WSManager.disconnect(websocket, room_name, user_name)