import logging
from .config import LOGTYPE


config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters":{
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "debug-log": {"handlers": ["default"], "level": "DEBUG"},
    },
}

class Logger():
    
    def __init__(self):
        self._logger = None
        self._mode : LOGTYPE = LOGTYPE.NULL 

    
    @property
    def logger(self): 

        return self._logger

    
    def initialize(self, mode:LOGTYPE, level:str='debug-log'):
        '''
        set logger
        :param mode: debug true or false
        :param: level: loggers name
        :return:
        '''

        self._logger = logging.getLogger(level)
        self._mode = mode


    def print(self, *args):
        '''
        console log
        :param args: contents
        :return:
        '''

        match self._mode:
            case LOGTYPE.DEBUG:
                self._logger.debug(args.__str__)
            case LOGTYPE.INFO:
                self._logger.info(args.__str__)
            case default:
                pass


logger = Logger()