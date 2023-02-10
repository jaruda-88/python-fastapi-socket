from os import path, environ
from enum import Enum
from pydantic import BaseModel

base_dir = path.dirname(path.dirname(path.abspath(__file__)))

class LOGTYPE(Enum):
    DEBUG = 1
    INFO = 2
    NULL = 3

class Config(BaseModel):
    ''' base configuration '''

    BASE_DIR: str = base_dir

    DEBUG: None | LOGTYPE


class ProdConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.NULL


class LocalConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.INFO


class TestConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.DEBUG


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