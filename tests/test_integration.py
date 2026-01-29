import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from fakeredis import FakeAsyncRedis, FakeServer
from sapphire_dispatcher import app

# Create a shared FakeServer so all redis instances share data
server = FakeServer()

def get_fake_redis(url, decode_responses=False):
    return FakeAsyncRedis(server=server, decode_responses=decode_responses)

@pytest.mark.asyncio
async def test_websocket_pubsub():
    # Patch the aioredis.from_url used in the app
    with patch("sapphire_dispatcher.aioredis.from_url", side_effect=get_fake_redis):
        client = TestClient(app)

        # We need to simulate the publish happening *after* the subscription.
        # Since TestClient.websocket_connect is synchronous-blocking context manager in sync tests,
        # but here we are using pytest-asyncio.
        # However, TestClient is synchronous.

        # TestClient creates a thread or uses starlette's test client which runs the app.
        # The websocket context manager yields the session.

        with client.websocket_connect("/ws/test-channel") as websocket:
            # At this point, the app should have subscribed to "test-channel"

            # Now we publish a message using the same fake redis server
            redis_publisher = FakeAsyncRedis(server=server, decode_responses=True)
            message_data = {"event": "test", "value": 123}
            await redis_publisher.publish("test-channel", json.dumps(message_data))

            # Receive from websocket
            data = websocket.receive_text()
            received_message = json.loads(data)

            assert received_message == message_data

            # Clean up
            await redis_publisher.aclose()

@pytest.mark.asyncio
async def test_websocket_multiple_messages():
    with patch("sapphire_dispatcher.aioredis.from_url", side_effect=get_fake_redis):
        client = TestClient(app)

        with client.websocket_connect("/ws/stream") as websocket:
            redis_publisher = FakeAsyncRedis(server=server, decode_responses=True)

            messages = ["msg1", "msg2", "msg3"]
            for msg in messages:
                await redis_publisher.publish("stream", json.dumps({"data": msg}))

            for msg in messages:
                data = websocket.receive_text()
                loaded = json.loads(data)
                assert loaded["data"] == msg

            await redis_publisher.aclose()
