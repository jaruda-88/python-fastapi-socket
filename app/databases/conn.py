from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from commons.logger import logger


class SQLAlchemy:

    def __init__(self, app: FastAPI = None, **kwargs):

        self._engine = None
        self._session = None

        if app is not None:
            self.initialize(app=app, **kwargs)

    
    def initialize(self, app: FastAPI, **kwargs):
        '''
        init db
        :parma app:
        :parma kwargs:
        :return:
        '''

        url = kwargs.get("DB_URL")

        if not url:
            logger.print('should be set db')
            return

        poolRecycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", True)

        self._engine = create_engine(
            url,
            echo=echo,
            pool_recycle=poolRecycle,
            pool_pre_ping=True
        )
        
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            logger.print("connected DB")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            logger.print("disconnected DB")

    
    def maintain_session(self):
        '''
        db session 유지 함수
        :return:
        '''

        if self._session is None:
            raise Exception("called initialize")

        s = None

        try:
            s = self._session()
            yield s
        finally:
            s.close()


    @property
    def session(self):
        
        return self.maintain_session

    
    @property
    def engine(self):

        return self._engine


db = SQLAlchemy()
base = declarative_base()