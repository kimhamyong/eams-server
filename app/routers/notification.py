from fastapi import APIRouter, WebSocket
from ws.websocket_server import websocket_endpoint

router = APIRouter()

# WebSocket 엔드포인트
@router.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket_endpoint(websocket)
