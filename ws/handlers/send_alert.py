from ws.websocket_server import manager

async def send_websocket_alert(alert_data: dict):
    """특정 gateway_id를 가진 클라이언트에게 알림 전송"""
    gateway_id = alert_data["gateway_id"]
    # 로그 추가
    print(f"📌 send_websocket_alert() 호출됨 - 현재 connected_clients: {manager.connected_clients}")
    print(f"📌 manager 객체 메모리 주소 (send_websocket_alert): {id(manager)}")
    await manager.send_to_gateway(gateway_id, alert_data)
