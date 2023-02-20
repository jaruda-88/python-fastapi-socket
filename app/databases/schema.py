from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func
)
from sqlalchemy.orm import Session, relationship
from conn import Base, db


class BaseSchema:
    id = Column(Integer, primary_key=True, index=True)
    create_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    update_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    # def __ini__(self):
    #     self._q = None
    #     self._session = None
    #     self.served = None


class Users(Base, BaseSchema):
    __tablename__ =  "users"

    pw = Column(String(length=2000), nullable=True)
    name = Column(String(length=255), nullable=True)