import asyncio
import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from redis import asyncio as aioredis
from starlette.websockets import WebSocketState

app = FastAPI(title="Sapphire Dispatcher")

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

@app.websocket("/ws/{channel_name}")
async def websocket_endpoint(websocket: WebSocket, channel_name: str):
    await websocket.accept()

    # Create a new Redis connection for each WebSocket client
    # In a production "Many-Worlds" scenario, we might want a connection pool
    # or a more sophisticated multiplexing strategy, but this ensures isolation.
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel_name)

    async def reader():
        """Reads from the WebSocket to detect disconnects."""
        try:
            while True:
                # We expect the client to be mostly silent (Observer),
                # but we must read to handle control frames and disconnects.
                await websocket.receive_text()
        except WebSocketDisconnect:
            # Normal disconnect
            pass
        except Exception as e:
            print(f"Error in reader: {e}")

    async def writer():
        """Reads from Redis and writes to the WebSocket."""
        try:
            async for message in pubsub.listen():
                if message["type"] == "message":
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await websocket.send_text(message["data"])
                    else:
                        break
        except Exception as e:
            print(f"Error in writer: {e}")

    try:
        reader_task = asyncio.create_task(reader())
        writer_task = asyncio.create_task(writer())

        # Run until one of them finishes (usually the reader on disconnect)
        done, pending = await asyncio.wait(
            [reader_task, writer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        # Cancel the pending task (e.g., stop listening to Redis if client left)
        for task in pending:
            task.cancel()

    except Exception as e:
        print(f"Error in websocket handler: {e}")
    finally:
        await pubsub.unsubscribe(channel_name)
        await redis.aclose()
        print(f"Client connection closed for channel {channel_name}")
