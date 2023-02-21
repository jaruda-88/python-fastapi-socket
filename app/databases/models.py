from databases.conn import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func
)
from sqlalchemy.orm import Session, relationship


class BaseModel:
    id = Column(Integer, primary_key=True, index=True)
    create_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    update_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())



class Users(Base, BaseModel):
    __tablename__ =  "tb_users"

    pw = Column(String(length=2000), nullable=True)
    name = Column(String(length=255), nullable=True)