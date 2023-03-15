from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from databases.handler import db
from databases.models import Users
from databases.schemas import UserRegister, Check
from commons.utils import get_hashed_password, verify_password

router = APIRouter(prefix="/user")


@router.post('/edit', status_code=200, response_model=Check)
async def modify(data: UserRegister, session: Session = Depends(db.session)):
    ''''''

    try:
        name = data.user_name

        user = Users.get(session, user_name=name)

        if user is None:
            raise Exception('incorrect user name')

        if not verify_password(data.password, user.password):
            raise Exception('incorrect password')

        user.user_name = data.user_name
        user.nick_name = data.nick_name
        user.password = get_hashed_password(data.password)
        session.commit()
    except Exception as ex:
        return JSONResponse(status_code=400, content=dict(msg=f"{ex.args[0]}"))
    else: 
        return True if user else False


# from fastapi import APIRouter, Depends
# from fastapi.security import OAuth2PasswordBearer
# from starlette.responses import JSONResponse
# from sqlalchemy.orm import Session
# from databases.handler import db
# from databases.models import Users
# from databases.schemas import Base, UserRegister

# router = APIRouter(prefix="/user")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# async def api_token(token: str = Depends(oauth2_scheme)):
#     if not token:
#         raise Exception('empty token')

# @router.post('/edit', dependencies=[Depends(api_token)], status_code=200, response_model=Base, tags=['user_management'])
# async def modify(data: UserRegister, session: Session = Depends(db.session)):
#     ''''''
#     return 'working'