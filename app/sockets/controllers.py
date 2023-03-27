from fastapi import WebSocket, Request
from starlette.websockets import WebSocketState
from manager import WSManager
from main import app
from databases.handler import db
from databases.models import Rooms, Members


@app.websocket("/ws/{room_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, room_id:int, user_id:int):

    try:
        room = Rooms.get(name=room_id)

        if not room:
            raise Exception('not found room')

        member = Members.filter(room_id__eq=room.id, user_id__eq=user_id)

        if not member:
            raise Exception(f'user:{user_id} is not in room:{room.name}')

        # add user
        await WSManager.connect(websocket, room_id, user_id)

        while True:

            if websocket.application_state == WebSocketState.CONNECTED:
                data = await websocket.receive_text()

                await WSManager.broadcast(f"{data}", member.rooms.name, member.users.nick_name)
    
    except Exception as ex:
        WSManager.disconnect(websocket, room_id, user_id)