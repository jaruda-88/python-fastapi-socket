import logging
import json
from collections import defaultdict

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, WebSocket, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates

from starlette.websockets import WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory='static'), name='static')

template = Jinja2Templates(directory="templates")

class WebSocketManager:

    def __init__(self):
        self.connectios: dict = defaultdict(dict)
        self.generator = self.get_getnerator()

    async def get_getnerator(self):
        while True:
            message = yield
            msg = message["message"]
            roomName = message["room_name"]
            await self._ws(msg, roomName)

    def get_members(self, room_name):
        try:
            return self.connectios[room_name]
        except Exception:
            return None

    async def push(self, msg: str, room_name: str = None):
        body = {"message": msg, "room_name": room_name}
        await self.generator.asend(body)

    async def connect(self, websocket: WebSocket, room_name: str):
        await websocket.accept()
        if self.connectios[room_name] == {} or len(self.connectios[room_name]) == 0:
            self.connectios[room_name] = []
        self.connectios[room_name].append(websocket)
        print(f"connected : {self.connectios[room_name]}")

    def remove(self, websocket: WebSocket, room_name: str):
        self.connectios[room_name].remove(websocket)
        print(f"connection remove : {self.connectios[room_name]}")


    async def _ws(self, message: str, room_name: str):
        living_connections = []
        while len(self.connectios[room_name]) > 0:

            websocket = self.connectios[room_name].pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connectios[room_name] = living_connections

