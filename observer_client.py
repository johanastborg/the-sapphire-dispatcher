import asyncio
import sys
import websockets

async def observer_connect(uri):
    """
    Connects to the Sapphire Dispatcher (WebSocket) and observes vibrations.
    """
    print(f"🔭 Next.js Observer: Tuning into {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to the Quantum Tunnel.")
            while True:
                message = await websocket.recv()
                print(f"⚡ Vibration received: {message}")
    except Exception as e:
        print(f"❌ Connection lost: {e}")

if __name__ == "__main__":
    channel_name = sys.argv[1] if len(sys.argv) > 1 else "universal-frequency"
    # Assuming default FastAPI port is 8000
    uri = f"ws://localhost:8000/ws/{channel_name}"

    try:
        asyncio.run(observer_connect(uri))
    except KeyboardInterrupt:
        print("\nDisconnected.")
