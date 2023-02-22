from databases.conn import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import Session, relationship


class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    create_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    update_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())



class Users(Base, BaseModel):
    __tablename__ =  "tb_users"

    pw = Column(String(length=2000), nullable=False)
    user_name = Column(String(length=255), nullable=False)
    nick_name = Column(String(length=255), nullable=True)


class Rooms(Base, BaseModel):
    __tablename__ = "tb_rooms"

    name = Column(String(length=255), nullable=False)


class Members(Base, BaseModel):
    __tablename__ = "tb_members"    

    user_id = Column(Integer, ForeignKey('tb_users.id'))
    room_id = Column(Integer, ForeignKey('tb_members.id'))


