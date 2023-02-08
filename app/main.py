import uvicorn
from fastapi import FastAPI
from dataclasses import asdict
from commons.config import conf, LOGTYPE
from commons.logger import logger
from routers.chats import index
from starlette.middleware.cors import CORSMiddleware


def create_app():
    '''
    init app
    :return:
    '''

    # load config
    dcConfig = conf()
    dictConf = asdict(dcConfig)
    debug : LOGTYPE = dictConf.get("DEBUG")

    app = FastAPI(debug= True if debug == LOGTYPE.DEBUG else False)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # set logger
    logger.initialize(mode=debug)

    # set router
    app.include_router(index.router) 

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)