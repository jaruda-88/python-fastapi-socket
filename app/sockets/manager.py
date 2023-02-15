from collections import defaultdict
from fastapi import WebSocket, Request, Depends, BackgroundTasks
from starlette.websockets import WebSocketDisconnect
from commons.logger import logger

class Manager:

    def __init__(self):
        self._connections = None


    def initialize(self):
        '''
        init
        '''
        self._connections: dict = defaultdict(dict)


    @property
    def connections(self):

        return self._connections

    
    @connections.setter
    def connections(self, room_name:str):

        if room_name not in self._connections:
            self._connections[room_name] = []

    
    async def connect(self, websocket: WebSocket, room_name:str, user_name:str):

        await websocket.accept()
        self.connections = room_name
        self._connections[room_name].append(websocket)
        logger.print(f"connected : {self._connections[room_name]}")

    
    def disconnect(self, websocket: WebSocket, room_name:str, user_name:str):

        self._connections[room_name].remove(websocket)
        logger.print(f"disconnecting : {self._connections[room_name]}")

    
    async def send_msg(self, message:str, websocket:WebSocket):

        await websocket.send_text(message)


    async def broadcast(self, message:str, room_name:str, user_name:str):

        for conn in self._connections[room_name]:
            await conn.send_text(message)


WSManager = Manager()