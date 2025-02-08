from fastapi import APIRouter, WebSocket
from ws.ws_server import websocket_endpoint

router = APIRouter()

@router.websocket("/ws/{gateway_id}/activity")
async def websocket_route_activity(websocket: WebSocket, gateway_id: str):
    """Activity WebSocket 연결"""
    await websocket_endpoint(websocket, gateway_id, "activity") 

@router.websocket("/ws/{gateway_id}/alert")
async def websocket_route_alert(websocket: WebSocket, gateway_id: str):
    """Alert WebSocket 연결"""
    await websocket_endpoint(websocket, gateway_id, "alert") 
