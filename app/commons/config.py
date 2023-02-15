from os import path, environ
from enum import Enum
from pydantic import BaseModel

base_dir = path.dirname(path.dirname(path.abspath(__file__)))
app_dir = path.dirname(path.dirname(__file__))


class LOGTYPE(Enum):
    TEST = 1
    DEBUG = 2
    INFO = 3
    NULL = 4


class Config(BaseModel):
    ''' base configuration '''

    BASE_DIR: str = base_dir
    APP_DIR: str = app_dir

    DEBUG: None | LOGTYPE


class ProdConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.NULL


class LocalConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.DEBUG


class TestConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.TEST


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