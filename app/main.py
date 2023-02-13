import uvicorn
from fastapi import FastAPI
from commons.config import conf, LOGTYPE
from commons.logger import logger
from routers.room_management import generation
from starlette.middleware.cors import CORSMiddleware
from sockets.manager import WSManager


def create_app():
    '''
    init app
    :return:
    '''

    # load config
    config = conf()

    app = FastAPI(debug = True if config.DEBUG == LOGTYPE.DEBUG or config.DEBUG == LOGTYPE.TEST else False)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # set logger
    logger.initialize(mode=config.DEBUG)

    # set websocket manager
    WSManager.initialize()

    # set router
    app.include_router(generation.router) 

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)