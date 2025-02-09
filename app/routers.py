from fastapi import APIRouter, WebSocket
from ws.ws_server import websocket_endpoint

# Initialize API router for WebSocket connections
router = APIRouter()

@router.websocket("/ws/{gateway_id}/activity")
async def websocket_route_activity(websocket: WebSocket, gateway_id: str):
    """Handles WebSocket connections for activity events.

    - Establishes a WebSocket connection for activity updates.
    - `gateway_id` specifies which gateway's activity data to receive.
    """
    await websocket_endpoint(websocket, gateway_id, "activity") 

@router.websocket("/ws/{gateway_id}/alert")
async def websocket_route_alert(websocket: WebSocket, gateway_id: str):
    """Handles WebSocket connections for alert notifications.

    - Establishes a WebSocket connection for real-time alerts.
    - `gateway_id` specifies which gateway's alert data to receive.
    """
    await websocket_endpoint(websocket, gateway_id, "alert")  
