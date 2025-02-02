from fastapi import APIRouter, WebSocket
from ws.handlers.send_alert import send_websocket_alert
from ws.websocket_server import websocket_endpoint

router = APIRouter()

# 테스트용 라우터 추가
@router.post("/send-alert")
async def send_alert(alert_data: dict):
    """JS에서 API 요청 시 WebSocket 메시지를 전송"""
    await send_websocket_alert(alert_data)
    return {"status": "sent", "gateway_id": alert_data["gateway_id"]}


@router.websocket("/ws/{gateway_id}/alert")
async def websocket_route(websocket: WebSocket, gateway_id: str):
    """WebSocket을 특정 Gateway ID로 연결 (Alert 전송)"""
    await websocket_endpoint(websocket, gateway_id)
