from fastapi import APIRouter, WebSocket, Request
from starlette.responses import Response

router = APIRouter()


@router.get("/{room_name}/{user_name}")
async def index(room_name, user_name):
    '''
    gen room
    :return: 
    '''
 
    return Response("success")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    # connected client 
    await websocket.accept()

    await websocket.send_text(f"welcome client : {websocket.client}")

    while True:
        # wait clinet message 
        data = await websocket.receive_text()

        print(f"message received : {data} from : {websocket.client}")

        await websocket.send_text(f"Message text was : {data}")