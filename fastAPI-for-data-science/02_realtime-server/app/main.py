import asyncio
import contextlib

from broadcaster import Broadcast
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect

broadcast = Broadcast("redis://localhost:6379")
CHANNEL = "CHAT"


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()


app = FastAPI(lifespan=lifespan)


class MessageEvent(BaseModel):
    username: str
    message: str


async def chat_publisher(websocket: WebSocket, username: str):
    """Listens for messages FROM the browser and publishes TO Redis."""
    try:
        while True:
            data = await websocket.receive_text()
            event = MessageEvent(username=username, message=data)
            await broadcast.publish(channel=CHANNEL, message=event.json())
    except Exception:
        pass


async def chat_subscriber(websocket: WebSocket):
    """Listens for messages FROM Redis and sends TO the browser."""
    async with broadcast.subscribe(channel=CHANNEL) as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, username: str = "Anonymous"):
    await websocket.accept()
    publisher_task = asyncio.create_task(chat_publisher(websocket, username))
    subscriber_task = asyncio.create_task(chat_subscriber(websocket))

    try:
        await asyncio.wait(
            [publisher_task, subscriber_task],
            return_when=asyncio.FIRST_COMPLETED
        )
    except Exception:
        pass
    finally:
        publisher_task.cancel()
        subscriber_task.cancel()