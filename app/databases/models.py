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

    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

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
        simple get a row
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

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        '''
        filter get a row
        :param session:
        :param kwargs: {'column__comparison operation':value}
        :return model:
        '''
        
        cond = []
        for key, val in kwargs.items():
            keys = key.split('__')
            
            if len(keys) > 2 or len(keys) != 2:
                raise Exception('key is out of form')

            col = getattr(cls, keys[0])

            match keys[1]:
                case 'eq':
                    cond.append((col == val))
                case 'gt':
                    cond.append((col > val))
                case 'ge':
                    cond.append((col >= val))
                case 'lt':
                    cond.append((col < val))
                case 'le':
                    cond.append((col <= val))
                case 'in':
                    cond.append((col.in_(val)))

        obj = cls()

        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False

        query = obj._session.query(cls)
        query = query.filter(*cond)

        obj._q = query

        return obj

    def update(self, auto_commit: bool = False, **kwargs):
        '''
        should be filter -> update row
        :param auto_commit:
        :param kwargs:
        :return row:
        '''

        qs = self._q.update(kwargs)
        result = None

        self._session.flush()

        if qs > 0:
            result = self._q.first()
        
        if auto_commit:
            self._session.commit()

        return result

    def first(self):
        '''
        should be filter -> first
        '''

        result = self._q.first()
        self.close()
        return result
    
    def all(self):
        '''
        should be filter -> all
        '''

        result = self._q.all()
        self.close()
        return result

    def count(self):
        '''
        should be filter -> count
        '''

        result = self._q.count()
        self.close()
        return result

    def delete(self, auto_commit: bool = False):
        '''
        should be filter -> delete
        '''

        self._q.delete()
        if auto_commit:
            self._session.commit()

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()



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
    room_id = Column(Integer, ForeignKey('tb_rooms.id'))

    users = relationship("Users")
    rooms = relationship("Rooms")


