from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from commons.utils import get_hashed_password
from databases.handler import db
from databases.models import Users
from databases.schemas import UserRegister, Base

router = APIRouter(prefix="/auth")


@router.post('/signup', status_code=201, response_model=Base, tags=["user_management"])
async def register(data: UserRegister, session: Session = Depends(db.session)):
    '''
    회원가입
    :param data:
    :param session:
    :return:
    '''

    try:
        hashPw = get_hashed_password(data.password)
        newUser = Users.create(session, True, user_name=data.user_name, nick_name=data.nick_name, password=hashPw)
    except Exception as ex:
        return JSONResponse(status_code=400, content=dict(msg=f"{ex.args[0]}"))
    else:
        return { 'id' : newUser.id }