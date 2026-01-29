# The Armstrong Universal Server: Sapphire Dispatcher

> *"The message router is the heart—it ensures that when a file is dropped into the Dark Matter Vault, every connected Next.js Observer feels the vibration instantly."*

## Overview

Welcome to the **Sapphire Dispatcher**, the high-frequency, low-latency pulsating core of the Armstrong Universal Server architecture. This component is responsible for the instantaneous propagation of state changes across the Many-Worlds continuum (your distributed container instances).

By leveraging **Redis Pub/Sub** over **WebSockets**, we transform the standard HTTP Quantum Tunnel into a bidirectional superhighway, ensuring that no observer is left in a stale universe.

## Architecture

The system consists of three primary celestial bodies:

1.  **Sapphire Dispatcher (The Hub)**:
    *   A FastAPI-based WebSocket server.
    *   Subscribes to Redis channels ("frequencies") on behalf of connected clients.
    *   Broadcasts messages to all observers tuned into a specific frequency.

2.  **Dark Matter Vault (The Producer)**:
    *   The origin of all truth.
    *   When an artifact (file) is deposited here, it emits a vibration (message) to the Redis ether.
    *   Ensures that the state is immutable and propagated instantly.

3.  **Next.js Observer (The Client)**:
    *   The end-user interface residing in the browser.
    *   Maintains a persistent WebSocket connection to the Sapphire Dispatcher.
    *   Updates the UI in real-time as vibrations are received.

## Lore & Mechanics

*   **Many-Worlds Consistency**: By using Redis as the backing store for Pub/Sub, we allow multiple instances of the Sapphire Dispatcher running on Cloud Run to share the same reality. A message published to one instance is received by all, ensuring that users connected to different containers still see the same events.
*   **Quantum Tunneling**: WebSockets provide the mechanism to bypass the request/response cycle, allowing server-initiated events to reach the client with zero friction.

## Installation & Deployment

### Prerequisites

*   Python 3.12+
*   Redis Server (The Ether)

### Setup

1.  **Initialize the Environment**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ignite the Sapphire Dispatcher**:
    ```bash
    uvicorn sapphire_dispatcher:app --reload
    ```
    The Dispatcher is now humming at `ws://localhost:8000/ws/{channel}`.

3.  **Tune in an Observer**:
    Open a terminal and run the observer client:
    ```bash
    python observer_client.py universal-frequency
    ```

4.  **Drop a Payload into the Vault**:
    In another terminal, simulate a file drop:
    ```bash
    python dark_matter_vault.py universal-frequency "Artifact #42 discovered"
    ```

    Watch as the Observer instantly reports the vibration!

## Testing the Fabric

To verify the integrity of the space-time continuum (integration tests):

```bash
PYTHONPATH=. pytest tests/
```

## Future Trajectories

*   **Authentication**: Secure the Quantum Tunnel with JWT tokens to prevent unauthorized inter-dimensional travel.
*   **Presence**: Track which Observers are currently tuned in.
*   **History**: Implement a stream to allow Observers to replay past events upon connection.

---

*"We don't just build servers. We build universes."*
