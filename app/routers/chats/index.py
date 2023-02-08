from fastapi import APIRouter
from starlette.responses import Response

router = APIRouter()


@router.get("/{room_name}/{user_name}")
async def index(room_name, user_name):
    '''
    gen room
    :return: 
    '''
 
    return Response("success")