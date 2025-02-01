import os
import json
import asyncio
from gmqtt import Client as MQTTClient
from dotenv import load_dotenv
from app.services.redis_service import save_activity

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

        # Redis에 데이터 저장 (서비스 모듈 사용)
        save_activity(gateway_id, sensor, timestamp)

        print(f"📩 MQTT Received: {data}")
    
    except Exception as e:
        print(f"❌ MQTT Data Processing Error: {e}")

async def start_mqtt():
    """MQTT 연결 및 구독 설정"""
    mqtt_client.on_message = on_message
    await mqtt_client.connect(BROKER, PORT)
    mqtt_client.subscribe(TOPIC, qos=0)
    print(f"✅ MQTT connected & subscribed to topic: {TOPIC}")
