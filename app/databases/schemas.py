from pydantic import BaseModel

class User(BaseModel):
    id: int 
    user_name: str

    class Config:
        orm_mode = True

class CreateUser(User):
    nick_name: str
    password: str
