from fastapi import WebSocket, WebSocketDisconnect
import json

# WebSocket에 연결된 클라이언트 (gateway_id 별로 관리)
connected_clients = {}

async def websocket_endpoint(websocket: WebSocket, gateway_id: str):
    """WebSocket 서버: 특정 gateway_id를 가진 클라이언트 연결"""
    await websocket.accept()
    
    # 특정 gateway_id에 대한 WebSocket 클라이언트 추가
    if gateway_id not in connected_clients:
        connected_clients[gateway_id] = set()
    connected_clients[gateway_id].add(websocket)
    
    print(f"✅ WebSocket 클라이언트 연결됨 (Gateway: {gateway_id})")

    try:
        while True:
            await websocket.receive_text()  # 메시지 수신 (사용 안 해도 유지 필요)
    except WebSocketDisconnect:
        print(f"❌ WebSocket 클라이언트 연결 종료 (Gateway: {gateway_id})")
        connected_clients[gateway_id].remove(websocket)
        if not connected_clients[gateway_id]:
            del connected_clients[gateway_id]  # 클라이언트가 없으면 key 삭제

async def send_websocket_activity(activity_data: dict):
    """특정 gateway_id를 가진 클라이언트에게 데이터 전송"""
    gateway_id = activity_data["gateway_id"]
    
    if gateway_id in connected_clients:
        message = json.dumps(activity_data)
        for client in connected_clients[gateway_id]:
            await client.send_text(message)
        print(f"🚀 WebSocket으로 데이터 전송 (Gateway: {gateway_id}): {message}")
    else:
        print(f"⚠️ WebSocket 클라이언트 없음 (Gateway: {gateway_id})")
