import os
import json
import redis
import asyncio
from gmqtt import Client as MQTTClient
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
TOPIC = os.getenv("MQTT_TOPIC")

# Redis 클라이언트 연결
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

mqtt_client = MQTTClient("mqtt_client")

async def on_message(client, topic, payload, qos, properties):
    """MQTT 메시지 수신 및 Redis 저장"""
    try:
        data = json.loads(payload.decode())  # JSON 변환
        gateway_id = data["gateway_id"]
        sensor = data["sensor"]
        timestamp = data["timestamp"]

        # 센서별 마지막 감지 시간 저장
        redis_key = f"user:{gateway_id}:{sensor}_activity"
        r.set(redis_key, timestamp)

        # 전체 활동 시간 업데이트 (가장 최근 감지된 시간)
        r.set(f"user:{gateway_id}:total_activity", timestamp)

        print(f"📩 MQTT Received & Saved to Redis: {data}")

    except json.JSONDecodeError:
        print(f"❌ Received Non-JSON message: {payload.decode()}")
    except Exception as e:
        print(f"❌ MQTT Data Processing Error: {e}")

async def start_mqtt():
    """MQTT 연결 및 구독 설정"""
    mqtt_client.on_message = on_message
    await mqtt_client.connect(BROKER, PORT)
    mqtt_client.subscribe(TOPIC, qos=0)
    print(f"✅ MQTT connected & subscribed to topic '{TOPIC}'")
