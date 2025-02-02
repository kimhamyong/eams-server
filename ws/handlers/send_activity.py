import json
from ws.websocket_server import connected_clients

async def send_websocket_activity(activity_data: dict):
    """Send activity data to a specific gateway_id's connected clients"""
    gateway_id = activity_data["gateway_id"]
    
    if gateway_id in connected_clients:
        message = json.dumps(activity_data)
        for client in connected_clients[gateway_id]:
            await client.send_text(message)
        print(f"🚀 WebSocket data sent (Gateway: {gateway_id}): {message}")
    else:
        print(f"⚠️ No WebSocket clients found (Gateway: {gateway_id})")
