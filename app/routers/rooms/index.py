from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from databases.handler import db
from databases.schemas import Base, RoomRegister
from databases.models import Users, Rooms, Members

router = APIRouter(prefix="/room")


@router.post('/create', status_code=201, response_model=Base)
async def register(data: RoomRegister, session: Session = Depends(db.session)):
    '''
    create room
    :param data:
    :param session:
    :return:
    '''

    try:
        room = Rooms.get(session, name=data.room_name)

        if room:
            raise Exception('already exists room name')
        
        newRoom = Rooms.create(session, True, name=data.room_name)

        filterUsers = Users.filter(session, id__in=tuple(data.user_ids))
        users = filterUsers.all()

        for user in users:
            
            filterMem = Members.filter(session, user_id__eq=user.id, room_id__eq=newRoom.id)
            member = filterMem.first()

            if member:
                raise Exception(f'already user:{user.user_name} in room:{newRoom.name}')

            Members.create(session, auto_commit=True, user_id=user.id, room_id=newRoom.id)

    except Exception as ex:
        return JSONResponse(status_code=400, content=dict(msg=f"{ex.args[0]}"))
    else:
        return dict(id=newRoom.id)


