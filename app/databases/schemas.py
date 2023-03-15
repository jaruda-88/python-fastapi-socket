from pydantic import BaseModel
from typing import List

class Base(BaseModel):
    id: int

class Check(BaseModel):
    verify: bool

class Token(BaseModel):
    authorization: str

class UserBase(BaseModel):
    user_name: str
    nick_name: str

    class Config:
        orm_mode = True

class UserRegister(UserBase):
    password: str

class UserInfo(UserBase, Base):
    created_at: str
    updated_at: str

class RoomRegister(BaseModel):
    user_ids: List[int] = []
    room_name: str
    

