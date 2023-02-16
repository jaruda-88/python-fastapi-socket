import os
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from commons.config import base_dir

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))


@router.get("/clinet/{room_name}/{user_name}")
async def test_clinet(request: Request, room_name, user_name):
    '''
    test client
    :return: 
    '''
 
    return templates.TemplateResponse("client.html", {"request":request, "room_name": room_name, "user_name": user_name})
