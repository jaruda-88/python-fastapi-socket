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
    def connections(self, room_id:int):

        if room_id not in self._connections:
            self._connections[room_id] = []

    
    async def connect(self, websocket: WebSocket, room_id:int, user_id:int):

        await websocket.accept()
        self.connections = room_id
        self._connections[room_id].append(websocket)
        logger.print(f"connected : {self._connections[room_id]}")

    
    def disconnect(self, websocket: WebSocket, room_id:int, user_id:int):

        self._connections[room_id].remove(websocket)
        logger.print(f"disconnecting : {self._connections[room_id]}")

    
    async def send_msg(self, message:str, websocket:WebSocket):

        await websocket.send_text(message)


    async def broadcast(self, message:str, room_name:str, user_name:str):

        for conn in self._connections[room_name]:
            await conn.send_text(message)


WSManager = Manager()