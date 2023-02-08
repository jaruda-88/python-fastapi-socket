from collections import defaultdict
from fastapi import WebSocket, Request, Depends, BackgroundTasks
from starlette.websockets import WebSocketDisconnect

class Manager:

    def __init__(self):
        self._connections: dict = defaultdict(dict)
        self._members: dict = defaultdict(dict)
    

    @property
    def connections(self):

        return self._connections

    
    @property 
    def members(self):

        return self._members

    
    @connections.setter
    def connections(self, room_name:str):

        if room_name != 0 and room_name not in self._connections:
            self._connections[room_name] = []

    
    async def connect(self, websocket: WebSocket, room_name:str, user_name:str):
        await websocket.accept()
        self.connections = room_name
        self._members[user_name] = websocket
        self._connections[room_name].append(websocket)
        print(f"connected : {self._connections[room_name]}")

    
    def remove(self, websocket: WebSocket, room_name:str, user_name:str):
        self._connections[room_name].remove(websocket)
        self._members.pop(user_name, None)
        print(f"disconnecting : {self._connections[room_name]}")

    
    async def send_msg(self, message:str, websocket:WebSocket):
        await websocket.send_text(message)


    async def broadcast(self, message:str, room_name:str):
        for conn in self._connections[room_name]:
            await conn.send_text(message)