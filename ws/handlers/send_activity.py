from ws.websocket_server import manager

async def send_websocket_activity(activity_data: dict):
    """특정 gateway_id를 가진 클라이언트에게 데이터 전송"""
    gateway_id = activity_data["gateway_id"]
    await manager.send_to_gateway(gateway_id, activity_data) 
