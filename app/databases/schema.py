from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    func
)
from sqlalchemy.orm import Session, relationship
from conn import base, db


class BaseSchema:
    id = Column(Integer, primary_key=True, index=True)
    create_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    update_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())

    def __ini__(self):
        self._q = None
        self._session = None
        self.served = None