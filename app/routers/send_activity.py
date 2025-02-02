from fastapi import APIRouter, WebSocket
from ws.websocket_server import websocket_endpoint

router = APIRouter()

@router.websocket("/ws/{gateway_id}")
async def websocket_route(websocket: WebSocket, gateway_id: str):
    """WebSocket을 특정 Gateway ID로 연결"""
    await websocket_endpoint(websocket, gateway_id)
