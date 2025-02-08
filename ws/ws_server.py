import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """WebSocket 연결을 관리하는 클래스"""
    
    def __init__(self):
        self.connected_clients = {
            "activity": {},  # ✅ Activity WebSocket 연결
            "alert": {}      # ✅ Alert WebSocket 연결
        }
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, gateway_id: str, ws_type: str):
        """특정 gateway_id와 WebSocket 타입(activity/alert)을 가진 클라이언트 연결"""
        await websocket.accept()
        async with self.lock:
            if ws_type not in self.connected_clients:
                print(f"❌ Invalid WebSocket type: {ws_type}")
                return
            
            if gateway_id not in self.connected_clients[ws_type]:
                self.connected_clients[ws_type][gateway_id] = set()
            
            # ✅ 기존 연결을 먼저 정리하고 새 WebSocket만 추가
            for client in list(self.connected_clients[ws_type][gateway_id]):
                if client.client_state != WebSocketState.CONNECTED:
                    self.connected_clients[ws_type][gateway_id].remove(client)

            self.connected_clients[ws_type][gateway_id].add(websocket)

        print(f"✅ WebSocket client connected (Gateway: {gateway_id}, Type: {ws_type})")
        print(f"📌 현재 연결된 clients: {self.connected_clients}")

    async def disconnect(self, websocket: WebSocket, gateway_id: str, ws_type: str):
        """특정 gateway_id와 WebSocket 타입(activity/alert)을 가진 클라이언트 연결 해제"""
        async with self.lock:
            if ws_type in self.connected_clients and gateway_id in self.connected_clients[ws_type]:
                self.connected_clients[ws_type][gateway_id].discard(websocket)
                if not self.connected_clients[ws_type][gateway_id]:  # 마지막 클라이언트가 해제되면 삭제
                    del self.connected_clients[ws_type][gateway_id]

        print(f"❌ WebSocket client disconnected (Gateway: {gateway_id}, Type: {ws_type})")
        print(f"📌 현재 연결된 clients: {self.connected_clients}")

    async def send_to_gateway(self, gateway_id: str, message: dict, ws_type: str):
        """특정 WebSocket 타입(activity 또는 alert)으로 메시지 전송"""
        async with asyncio.Lock():
            if ws_type not in self.connected_clients:
                print(f"❌ Invalid WebSocket type: {ws_type}")
                return
            
            print(f"📌 메시지 전송 시점의 connected_clients 상태: {self.connected_clients[ws_type]}")
            if gateway_id in self.connected_clients[ws_type]:
                message_json = json.dumps(message)
                for client in list(self.connected_clients[ws_type][gateway_id]):  # ✅ 복사본 사용 (에러 방지)
                    try:
                        await client.send_text(message_json)
                        print(f"✅ Message sent to {gateway_id} ({ws_type}): {message_json}")
                    except Exception as e:
                        print(f"❌ WebSocket send failed (Gateway: {gateway_id}, Type: {ws_type}): {e}")
                        await self.disconnect(client, gateway_id, ws_type)  # 비정상 연결 제거
            else:
                print(f"❌ No active WebSocket clients for Gateway {gateway_id} ({ws_type})")

# ✅ 웹소켓 매니저 인스턴스 생성
manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, gateway_id: str, ws_type: str):
    """WebSocket 엔드포인트"""
    await manager.connect(websocket, gateway_id, ws_type)
    try:
        while True:
            await websocket.receive_text()  # 연결 유지
    except WebSocketDisconnect:
        await manager.disconnect(websocket, gateway_id, ws_type)
