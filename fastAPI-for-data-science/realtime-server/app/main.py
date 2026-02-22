import asyncio
from datetime import datetime

from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect


app = FastAPI()


async def echo_message(websocket: WebSocket):
    data = await websocket.receive_text()
    await websocket.send_text(data)


async def send_time(websocket: WebSocket):
    await asyncio.sleep(10)
    await websocket.send_text(datetime.utcnow().isoformat())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            task_echo_message = asyncio.create_task(echo_message(websocket))
            task_send_time = asyncio.create_task(send_time(websocket))
            done, pending = await asyncio.wait(
                {task_echo_message, task_send_time}, return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()
            for task in done:
                task.result()

    except WebSocketDisconnect:
        pass
