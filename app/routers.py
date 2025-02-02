from fastapi import APIRouter, WebSocket
from ws.ws_server import websocket_endpoint

router = APIRouter()

@router.websocket("/ws/{gateway_id}/activity")
async def websocket_route(websocket: WebSocket, gateway_id: str):
    """WebSocket을 특정 Gateway ID로 연결"""
    await websocket_endpoint(websocket, gateway_id)

@router.websocket("/ws/{gateway_id}/alert")
async def websocket_route(websocket: WebSocket, gateway_id: str):
    """WebSocket을 특정 Gateway ID로 연결 (Alert 전송)"""
    await websocket_endpoint(websocket, gateway_id)
