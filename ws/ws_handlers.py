from ws.ws_server import manager

async def send_websocket_alert(alert_data: dict):
    """Sends an alert message to the WebSocket clients of a specific gateway.

    - Extracts `gateway_id` from `alert_data`.
    - Uses `manager.send_to_gateway()` to send the alert message.
    - Message type is set to `"alert"`.
    """
    gateway_id = alert_data["gateway_id"]
    await manager.send_to_gateway(gateway_id, alert_data, "alert")

async def send_websocket_activity(activity_data: dict):
    """Sends an activity update to the WebSocket clients of a specific gateway.

    - Extracts `gateway_id` from `activity_data`.
    - Uses `manager.send_to_gateway()` to send the activity update.
    - Message type is set to `"activity"`.
    """
    gateway_id = activity_data["gateway_id"]
    await manager.send_to_gateway(gateway_id, activity_data, "activity")
