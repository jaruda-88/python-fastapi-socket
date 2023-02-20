import logging
import sys
from .config import LOGTYPE


config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
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
        "info-log": {"handlers": ["default"], "level": "INFO"},
    },
}

class Logger():
    
    def __init__(self):

        self._logger = None
        self._mode : LOGTYPE = LOGTYPE.NULL 

    
    @property
    def logger(self): 

        return self._logger

    
    def initialize(self, mode:LOGTYPE):
        '''
        set logger
        :param mode: debug true or false
        :param: level: loggers name
        :return:
        '''

        self._mode = mode
        match mode:
            case LOGTYPE.INFO:
                self._logger = logging.getLogger('info-log')
            case LOGTYPE.DEBUG:
                self._logger = logging.getLogger('debug-log')


    def print(self, *args):
        '''
        console log
        :param args: contents
        :return:
        '''

        match self._mode:
            case LOGTYPE.DEBUG:
                self._logger.debug(', '.join(args))
            case LOGTYPE.INFO:
                self._logger.info(', '.join(args))
            case LOGTYPE.TEST:
                print(', '.join(args), file=sys.stderr)

    
logger = Logger()