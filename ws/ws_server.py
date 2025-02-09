import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """Manages WebSocket connections for activity and alert messages.

    - Stores connected clients categorized by `activity` and `alert` WebSocket types.
    - Uses an asyncio lock to ensure thread safety when modifying connections.
    """

    def __init__(self):
        """Initializes WebSocket connection storage and a thread-safe lock."""
        self.connected_clients = {
            "activity": {},  # Stores activity WebSocket connections
            "alert": {}      # Stores alert WebSocket connections
        }
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, gateway_id: str, ws_type: str):
        """Establishes a WebSocket connection for a specific `gateway_id` and `ws_type`.

        - Accepts the WebSocket connection.
        - Ensures only active connections are stored.
        - Manages connections per `gateway_id` to avoid stale clients.
        """
        await websocket.accept()
        async with self.lock:
            if ws_type not in self.connected_clients:
                print(f"❌ Invalid WebSocket type: {ws_type}")
                return

            if gateway_id not in self.connected_clients[ws_type]:
                self.connected_clients[ws_type][gateway_id] = set()

            # Remove stale connections and add the new WebSocket connection
            for client in list(self.connected_clients[ws_type][gateway_id]):
                if client.client_state != WebSocketState.CONNECTED:
                    self.connected_clients[ws_type][gateway_id].remove(client)

            self.connected_clients[ws_type][gateway_id].add(websocket)

        print(f"✅ WebSocket client connected (Gateway: {gateway_id}, Type: {ws_type})")
        print(f"📌 Active WebSocket connections: {self.connected_clients}")

    async def disconnect(self, websocket: WebSocket, gateway_id: str, ws_type: str):
        """Removes a WebSocket connection for a specific `gateway_id` and `ws_type`.

        - If all clients for a gateway disconnect, the gateway entry is removed.
        """
        async with self.lock:
            if ws_type in self.connected_clients and gateway_id in self.connected_clients[ws_type]:
                self.connected_clients[ws_type][gateway_id].discard(websocket)
                if not self.connected_clients[ws_type][gateway_id]:  # Remove empty gateway entries
                    del self.connected_clients[ws_type][gateway_id]

        print(f"❌ WebSocket client disconnected (Gateway: {gateway_id}, Type: {ws_type})")
        print(f"📌 Active WebSocket connections: {self.connected_clients}")

    async def send_to_gateway(self, gateway_id: str, message: dict, ws_type: str):
        """Sends a message to all WebSocket clients under the given `gateway_id` and `ws_type`.

        - Converts the message to JSON format.
        - Iterates through connected clients and attempts to send the message.
        - Removes disconnected clients upon failure.
        """
        async with asyncio.Lock():
            if ws_type not in self.connected_clients:
                print(f"❌ Invalid WebSocket type: {ws_type}")
                return

            print(f"📌 Sending message, current connections: {self.connected_clients[ws_type]}")
            if gateway_id in self.connected_clients[ws_type]:
                message_json = json.dumps(message)
                for client in list(self.connected_clients[ws_type][gateway_id]):  # Use a copy to avoid iteration issues
                    try:
                        await client.send_text(message_json)
                        print(f"✅ Message sent to {gateway_id} ({ws_type}): {message_json}")
                    except Exception as e:
                        print(f"❌ WebSocket send failed (Gateway: {gateway_id}, Type: {ws_type}): {e}")
                        await self.disconnect(client, gateway_id, ws_type)  # Remove faulty connection
            else:
                print(f"❌ No active WebSocket clients for Gateway {gateway_id} ({ws_type})")

# Create a global WebSocket manager instance
manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, gateway_id: str, ws_type: str):
    """Handles WebSocket connection lifecycle for a given `gateway_id` and `ws_type`.

    - Connects the WebSocket client to the manager.
    - Keeps the connection alive by continuously listening for messages.
    - Cleans up the connection upon disconnection.
    """
    await manager.connect(websocket, gateway_id, ws_type)
    try:
        while True:
            await websocket.receive_text()  # Maintain connection by waiting for incoming messages
    except WebSocketDisconnect:
        await manager.disconnect(websocket, gateway_id, ws_type)
