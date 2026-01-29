import asyncio
import os
import sys
import json
import time
from redis import asyncio as aioredis

# Redis Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

async def drop_file_into_vault(channel: str, data: dict):
    """
    Simulates dropping a file into the Dark Matter Vault.
    This triggers a vibration (message) across the specified channel.
    """
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)

    message = json.dumps(data)
    await redis.publish(channel, message)
    print(f"🌀 Dark Matter Vault: Dropped payload into '{channel}': {message}")

    await redis.aclose()

if __name__ == "__main__":
    channel_name = sys.argv[1] if len(sys.argv) > 1 else "universal-frequency"
    payload_content = sys.argv[2] if len(sys.argv) > 2 else "New quantum state detected"

    payload = {
        "event": "file_dropped",
        "content": payload_content,
        "timestamp": time.time()
    }

    asyncio.run(drop_file_into_vault(channel_name, payload))
