import os
import json
import asyncio
from gmqtt import Client as MQTTClient
from dotenv import load_dotenv
from app.redis import save_activity
from ws.ws_handlers import send_websocket_activity
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
TOPIC = os.getenv("MQTT_TOPIC")

mqtt_client = MQTTClient("mqtt_client")

async def on_message(client, topic, payload, qos, properties):
    """MQTT 메시지 수신 처리"""
    try:
        data = json.loads(payload.decode())
        gateway_id = data["gateway_id"]
        sensor = data["sensor"]
        timestamp = data["timestamp"]

        # Redis에 데이터 저장
        save_activity(gateway_id, sensor, timestamp)

        # ✅ WebSocket을 통해 클라이언트에 전송
        activity_data = {
            "gateway_id": gateway_id,
            "sensor": sensor,
            "timestamp": timestamp
        }
        print(f"📩 MQTT Received: {data}")
        await send_websocket_activity(activity_data)
    
    except Exception as e:
        print(f"❌ MQTT Data Processing Error: {e}")

async def start_mqtt():
    """MQTT 연결 및 구독 설정"""
    mqtt_client.on_message = on_message
    await mqtt_client.connect(BROKER, PORT)
    mqtt_client.subscribe(TOPIC, qos=0)
    print(f"✅ MQTT connected & subscribed to topic: {TOPIC}")
