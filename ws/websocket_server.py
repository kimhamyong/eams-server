import asyncio
import json
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    """WebSocket 연결을 관리하는 클래스"""
    
    def __init__(self):
        self.connected_clients = {}  # {gateway_id: set(WebSocket)}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, gateway_id: str):
        """특정 gateway_id를 가진 클라이언트 연결"""
        await websocket.accept()
        async with self.lock:
            if gateway_id not in self.connected_clients:
                self.connected_clients[gateway_id] = set()
            self.connected_clients[gateway_id].add(websocket)
        print(f"✅ WebSocket client connected (Gateway: {gateway_id}) - Active connections: {len(self.connected_clients[gateway_id])}")

    async def disconnect(self, websocket: WebSocket, gateway_id: str):
        """특정 gateway_id를 가진 클라이언트 연결 해제"""
        async with self.lock:
            if gateway_id in self.connected_clients:
                self.connected_clients[gateway_id].discard(websocket)  # KeyError 방지
                if not self.connected_clients[gateway_id]:  # 해당 gateway_id에 클라이언트가 없으면 삭제
                    del self.connected_clients[gateway_id]
        print(f"❌ WebSocket client disconnected (Gateway: {gateway_id})")

    async def send_to_gateway(self, gateway_id: str, message: dict):
        """특정 gateway_id를 가진 모든 클라이언트에게 메시지 전송"""
        async with self.lock:
            if gateway_id in self.connected_clients:
                message_json = json.dumps(message)
                for client in self.connected_clients[gateway_id]:
                    try:
                        await client.send_text(message_json)
                    except Exception as e:
                        print(f"⚠️ WebSocket send failed (Gateway: {gateway_id}): {e}")
                        await self.disconnect(client, gateway_id)  # 비정상 연결 제거
                print(f"🚀 Sent message to Gateway {gateway_id}: {message_json}")
            else:
                print(f"⚠️ No active WebSocket clients for Gateway {gateway_id}")

# ✅ 웹소켓 매니저 인스턴스 생성 (이걸 다른 파일에서 가져와서 사용 가능)
manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, gateway_id: str):
    """WebSocket 엔드포인트"""
    await manager.connect(websocket, gateway_id)
    try:
        while True:
            await websocket.receive_text()  # 연결 유지
    except WebSocketDisconnect:
        await manager.disconnect(websocket, gateway_id)
