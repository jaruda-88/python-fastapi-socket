from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")

class WSConnectionMgr:
    def __init__(self):
        self.active_connection: List[WebSocket] = []

    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)

    
    def disconnect(self, websocket: WebSocket):
        self.active_connection.remove(websocket)

    
    async def send_msg(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    
    async def broadcast(self, message: str):
        for connection in self.active_connection:
            await connection.send_text(message)


manager = WSConnectionMgr()

@app.get("/client2")
async def clinet(request: Request):
    return templates.TemplateResponse("client2.html", {"request":request})

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_msg(f"you wrote: {data}", websocket)
            await manager.broadcast(f"say {client_id} : {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Clinet {client_id} left")

def run():
    import uvicorn
    uvicorn.run(app)

if __name__ == "__main__":
    run()