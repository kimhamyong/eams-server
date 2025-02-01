import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

def get_redis_client():
    """Redis 클라이언트 생성 및 반환"""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def save_activity(gateway_id: str, sensor: str, timestamp: str):
    """센서별 마지막 감지 시간 저장"""
    r = get_redis_client()
    redis_key = f"user:{gateway_id}:{sensor}_activity"
    r.set(redis_key, timestamp)

    """전체 활동 시간 업데이트 (가장 마지막 감지된 값 사용)"""
    r.set(f"user:{gateway_id}:total_activity", timestamp)

def get_last_activity(gateway_id: str, sensor: str):
    """센서별 마지막 감지 시간 조회"""
    r = get_redis_client()
    redis_key = f"user:{gateway_id}:{sensor}_activity"
    return r.get(redis_key)

def get_total_activity(gateway_id: str):
    """전체 센서의 마지막 감지 시간 조회"""
    r = get_redis_client()
    return r.get(f"user:{gateway_id}:total_activity")
