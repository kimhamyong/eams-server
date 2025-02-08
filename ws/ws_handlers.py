from ws.ws_server import manager

async def send_websocket_alert(alert_data: dict):
    """특정 gateway_id의 alert WebSocket으로 메시지 전송"""
    gateway_id = alert_data["gateway_id"]
    await manager.send_to_gateway(gateway_id, alert_data, "alert")

async def send_websocket_activity(activity_data: dict):
    """특정 gateway_id의 activity WebSocket으로 메시지 전송"""
    gateway_id = activity_data["gateway_id"]
    await manager.send_to_gateway(gateway_id, activity_data, "activity")  
