import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from commons.config import conf, LOGTYPE
from commons.logger import logger
from routers.rooms import test_client
from routers.users import (auth, verify, update)
from starlette.middleware.cors import CORSMiddleware
from sockets.manager import WSManager
from databases import handler, models
from commons.utils import api_token


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

    # set database
    handler.db.initialize(
        app, 
        DB_URL=config.get_db_url(), 
        DB_POOL_RECYCLE=config.DB_POOL_RECYCLE, 
        DB_ECHO=config.DB_ECHO
        )
    # set models
    models.Base.metadata.create_all(bind=handler.db.engine)

    # set websocket manager
    WSManager.initialize()

    # set router
    if config.DEBUG == LOGTYPE.TEST:
        app.include_router(test_client.router) 
    app.include_router(auth.router, tags=["user_management"])
    app.include_router(verify.router, tags=["user_management"])
    app.include_router(update.router, tags=['user_management'], dependencies=[Depends(api_token)])

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)