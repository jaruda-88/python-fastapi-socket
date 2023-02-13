from fastapi import APIRouter
from starlette.responses import Response
from sockets.manager import WSManager

router = APIRouter()


@router.get("/{room_name}/{user_name}")
async def in_room(room_name, user_name):
    '''
    gen room
    :return: 
    '''

    WSManager.connections = room_name
 
    return Response("success")