from databases.handler import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import Session, relationship
from databases.handler import db


class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def __hash__(self):
        return hash(self.id)

    def __columns__(self):
        return [ c for c in self.__table__.columns if c.primary_key is False and c.name != "created_at"]
    
    @classmethod
    def create(cls, session: Session, auto_commit=False, **kwargs):
        '''
        생성 전용 함수
        :param session: db session
        :param auto_commit: 자동 커밋
        :param kwargs: data
        :return:
        '''

        obj = cls()
        for col in obj.__columns__():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.flush()
        if auto_commit:
            session.commit()
        
        return obj

    @classmethod
    def get(cls, session: Session = None, **kwargs):
        '''
        get a row
        :param session:
        :param kwargs:
        :return:
        '''

        s = next(db.session()) if not session else session
        query = s.query(cls)

        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)

        if query.count() > 1:
            raise Exception('Only one row')
        
        result = query.first()

        if not session:
            s.close()

        return result


class Users(Base, BaseModel):
    __tablename__ =  "tb_users"

    password = Column(String(length=2000), nullable=False)
    user_name = Column(String(length=255), nullable=False)
    nick_name = Column(String(length=255), nullable=True)


class Rooms(Base, BaseModel):
    __tablename__ = "tb_rooms"

    name = Column(String(length=255), nullable=False)


class Members(Base, BaseModel):
    __tablename__ = "tb_members"    

    user_id = Column(Integer, ForeignKey('tb_users.id'))
    room_id = Column(Integer, ForeignKey('tb_members.id'))


