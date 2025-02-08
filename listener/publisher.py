import redis
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")  # 기본값을 'redis'로 설정
REDIS_PORT = int(os.getenv("REDIS_PORT"))

def get_redis_client():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def redis_expire_listener():
    """TTL 만료 감지 후 데이터 확인 및 alert_channel에 메시지 발행"""
    r = get_redis_client()
    pubsub = r.pubsub()
    pubsub.psubscribe("__keyevent@0__:expired")

    print("📡 Listening for expired keys...")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message and message["type"] == "pmessage":
            expired_key = message["data"]

            # 특정 Gateway ID 추출 (예: home1:total_activity → home1)
            if expired_key.endswith(":total_activity"):
                gateway_id = expired_key.split(":")[0]

                # ✅ TTL 만료 후 1초 대기 후 Redis 확인
                await asyncio.sleep(1.0)

                # ✅ 해당 게이트웨이(home1)에 남아 있는 모든 데이터 확인
                remaining_keys = r.keys(f"{gateway_id}:*")

                if not remaining_keys:  # ✅ 모든 데이터가 삭제된 경우에만 `alert` 전송
                    r.publish("alert_channel", gateway_id)
                    print(f"📢 Published Alert for Gateway: {gateway_id}")
                else:
                    print(f"⏳ TTL expired but {gateway_id} still has data: {remaining_keys}")
        
        await asyncio.sleep(0.1)  # ✅ 이벤트 루프 블로킹 방지

async def start_publisher():
    """TTL 감지 Publisher 실행"""
    asyncio.create_task(redis_expire_listener())  # ✅ 독립 실행
