from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from commons.utils import get_hashed_password, verify_password, create_access_token
from databases.handler import db
from databases.models import Users
from databases.schemas import UserRegister, Base, Token

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
        return dict(id=newUser.id)


@router.post('/signin', status_code=200, response_model=Token, tags=["user_management"])
async def login(data: OAuth2PasswordRequestForm = Depends()):
    '''
    로그인
    :param data:
    :param session:
    :return:
    '''

    try:
        name, pwd = data.username, data.password

        user = Users.get(user_name=name)

        if user is None:
            raise Exception('incorrect user info')

        if not verify_password(pwd, user.password):
            raise Exception('incorrect password')
        
        token = create_access_token(user.user_name)

    except Exception as ex:
        return JSONResponse(status_code=400, content=dict(msg=f"{ex.args[0]}"))
    else:
        return dict(authorization=token)

