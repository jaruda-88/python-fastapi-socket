import os
from fastapi import APIRouter, WebSocket, Request
from starlette.responses import Response
from fastapi.templating import Jinja2Templates
from sockets.manager import WSManager
from commons.config import app_dir

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(app_dir, "templates"))


@router.get("clinet/{room_name}/{user_name}")
async def test(request: Request, room_name, user_name):
    '''
    test client
    :return: 
    '''
 
    return templates.TemplateResponse("client.html", {"request":request, "room_name": room_name, "user_name": user_name})


# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):

#     # connected client 
#     await websocket.accept()

#     await websocket.send_text(f"welcome client : {websocket.client}")

#     while True:
#         # wait clinet message 
#         data = await websocket.receive_text()

#         print(f"message received : {data} from : {websocket.client}")

#         await websocket.send_text(f"Message text was : {data}")