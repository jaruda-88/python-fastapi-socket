# from fastapi import APIRouter, Depends
# from fastapi.security import APIKeyHeader
# from starlette.responses import JSONResponse
# from sqlalchemy.orm import Session
# from databases.handler import db
# from databases.models import Users
# from databases.schemas import UserRegister, Check
# from commons.utils import get_hashed_password

# router = APIRouter(prefix="/user")

# async def api_token(token: str = Depends(APIKeyHeader(name="token"))):
#     if not token:
#         raise Exception('empty token')

# @router.post('/edit', dependencies=[Depends(api_token)], status_code=200, response_model=Check, tags=['user_management'])
# async def modify(data: UserRegister, session: Session = Depends(db.session)):
#     ''''''

#     try:
#         name = data.user_name
#         hashPwd = get_hashed_password(data.password)
        
#         updateData = dict(user_name=data.user_name, nick_name=data.nick_name, password=hashPwd)
#         result = Users.update(update=updateData, user_name=name, password=hashPwd)
#     except Exception as ex:
#         return JSONResponse(status_code=400, content=dict(msg=f"{ex.args[0]}"))
#     else: 
#         return True if result else False


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