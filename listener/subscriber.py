import asyncio
import redis
from ws.ws_handlers import send_websocket_alert
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")  # 기본값을 'redis'로 설정
REDIS_PORT = int(os.getenv("REDIS_PORT"))

def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def subscribe_alerts():
    """Redis Pub/Sub에서 alert_channel을 비동기적으로 구독"""
    r = get_redis_client()
    pubsub = r.pubsub()
    pubsub.subscribe("alert_channel")

    print("📡 Subscribing to alert_channel...")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            gateway_id = message["data"]
            
            # ✅ Redis에서 해당 gateway_id 관련 데이터가 남아 있는지 확인
            remaining_keys = r.keys(f"{gateway_id}:*")
            
            if not remaining_keys:  # ✅ 모든 데이터가 삭제된 경우에만 WebSocket 전송
                alert_data = {
                    "gateway_id": gateway_id,
                    "message": "no activity detected"
                }
                await send_websocket_alert(alert_data)
                print(f"🚨 Sent WebSocket Alert: {alert_data}")
            else:
                print(f"⏳ Alert received but data still exists for {gateway_id}, skipping alert.")
        
        await asyncio.sleep(0.1)  # ✅ CPU 점유율을 낮추기 위해 대기

async def start_subscriber():
    """Subscriber를 독립적인 태스크로 실행"""
    asyncio.create_task(subscribe_alerts())  # ✅ 독립 실행하여 FastAPI를 블로킹하지 않음
