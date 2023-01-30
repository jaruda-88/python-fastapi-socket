from fastapi import FastAPI, WebSocket, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger


app = FastAPI()

templates = Jinja2Templates(directory="templates")

# test web page - http://127.0.0.1:8000/client
@app.get("/client")
async def client(request: Request):
    # /templates/client.html 
    return templates.TemplateResponse("client.html", {"request":request})


# web socket set - ws://127.0.0.1:8000/ws
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(f"clinet connected : {websocket.client}")

    await websocket.accept() # client의 websocket접속 허용

    await websocket.send_text(f"Welcome clinet : {websocket.client}")

    while True:
        data = await websocket.receive_text() # client 메세지 수신 대기

        print(f"message received : {data} from : {websocket.client}")

        await websocket.send_text(f"Message text was: {data}") # client에 메시지 전달


def run(): 
    import uvicorn
    uvicorn.run(app)


if __name__ == "__main__":
    run()
