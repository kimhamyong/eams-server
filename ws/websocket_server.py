from fastapi import WebSocket, WebSocketDisconnect
import json

# 현재 연결된 WebSocket 클라이언트 목록
connected_clients = set()

async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 서버: 클라이언트와 실시간 통신"""
    await websocket.accept()
    connected_clients.add(websocket)
    print("✅ WebSocket 클라이언트 연결됨")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("❌ WebSocket 클라이언트 연결 종료")
        connected_clients.remove(websocket)

async def send_websocket_alert(alert_message: dict):
    """현재 연결된 모든 클라이언트에 긴급 알림 전송"""
    if connected_clients:
        for client in connected_clients:
            await client.send_json(alert_message)
            print(f"🚨 WebSocket 알림 전송: {alert_message}")
