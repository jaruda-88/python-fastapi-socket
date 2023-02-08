from dataclasses import dataclass
from os import path, environ
from enum import Enum

base_dir = path.dirname(path.dirname(path.abspath(__file__)))

class LOGTYPE(Enum):
    DEBUG = 1
    INFO = 2
    NULL = 3

@dataclass
class Config:
    ''' base configuration '''

    BASE_DIR = base_dir

    DEBUG: LOGTYPE = LOGTYPE.NULL


@dataclass
class ProdConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.NULL


@dataclass
class LocalConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.INFO


@dataclass
class TestConfig(Config):
    DEBUG: LOGTYPE = LOGTYPE.DEBUG


def conf():
    '''
    load environment
    :return:
    '''

    config = dict(prod=ProdConfig(), local=LocalConfig(), test=TestConfig())
    # dict = asdict(TestConfig())
    return config.get(environ.get("API_ENV", "test"))