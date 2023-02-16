from os import path, environ
from enum import Enum
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Any

subclass_registry = {}
base_dir = path.dirname(path.dirname(path.abspath(__file__)))

'''
동기
$ pip install fastapi-sqlalchemy  # https://github.com/mfreeborn/fastapi-sqlalchemy
$ pip install pymysql
'''
db_url = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4"   # user, password, host, port, dbname
'''
비동기
$ pip install 'sqlalchemy[asyncio]'
$ pip install aiomysql
'''
async_db_url = "mysql+aiomysql://{}:{}@{}:{}/{}?charset=utf8mb4"    # user, password, host, port, dbname


class LOGTYPE(Enum):
    TEST = 1
    DEBUG = 2
    INFO = 3
    NULL = 4


class ModifiedBaseModel(BaseModel):
    def __init_subclass__(cls, is_abstract: bool = False, **kwargs:Any) -> None:
        super().__init_subclass__(**kwargs)  
        if not is_abstract:
            subclass_registry[cls.__name__] = cls


class Config(ModifiedBaseModel, ABC, is_abstract=True):
    ''' base configuration '''

    BASE_DIR: str = base_dir

    DEBUG: None | LOGTYPE = LOGTYPE.NULL

    DB_USER: None | str = environ.get("MYSQL_USER", None)
    DB_PWD: None | str = environ.get("MYSQL_PASSWORD", None)
    DB_NAME: None | str = environ.get("MYSQL_DATABASE", None)
    DB_ECHO: bool = True
    DB_POOL_RECYCLE: int = 900

    @abstractmethod
    def get_db_url(self) -> None | str:
        raise NotImplementedError


class ProdConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.NULL
    
    def get_db_url(self) -> None | str:
        return None


class LocalConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.DEBUG

    def get_db_url(self) -> None | str:
        return None


class TestConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.TEST
    
    def get_db_url(self) -> None | str:
        return db_url.format(self.DB_USER, self.DB_PWD, '192.168.0.100', 3307, self.DB_NAME) if self.DB_NAME else None


def conf():
    '''
    load environment
    :return:
    '''

    match environ.get("API_ENV", "test"):
        case "prod":
            return ProdConfig()
        case "local":
            return LocalConfig()
        case "test":
            return TestConfig()