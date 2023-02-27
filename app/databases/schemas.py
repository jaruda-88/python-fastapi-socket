from pydantic import BaseModel

class Base(BaseModel):
    id: int


# class User(BaseModel):

#     class Config:
#         orm_mode = True

class UserRegister(BaseModel):
    user_name: str
    nick_name: str
    password: str

    class Config:
        orm_mode = True
