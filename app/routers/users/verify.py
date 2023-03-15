from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from databases.handler import db
from databases.models import Users
from databases.schemas import Check

router = APIRouter(prefix="/user")


@router.get('/check/{name}', status_code=200, response_model=Check)
async def check_user_name(name: str, session: Session = Depends(db.session)):
    '''
    check user_name
    :param name:
    :param session:
    :return:
    '''

    try:
        result = Users.get(session, user_name=name)
    except Exception as ex:
        return JSONResponse(status_code=400, content=dict(msg=f"{ex.args[0]}"))
    else:
        return dict(verify=True if result else False) 


@router.get('/check/{nick}', status_code=200, tags=["user_management"], response_model=Check)
async def check_nick_name(nick: str, session: Session = Depends(db.session)):
    '''
    check nick_name
    :param nick:
    :param session:
    :retrun:
    '''

    try:
        result = Users.get(session, nick_name=nick)
    except Exception as ex:
        return JSONResponse(status_code=400, content=dict(msg=f"{ex.args[0]}"))
    else:
        return dict(verify=True if result else False) 