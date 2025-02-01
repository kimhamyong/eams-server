from fastapi import APIRouter
import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

router = APIRouter()

@router.get("/last-activity/{gateway_id}/{sensor}")
async def get_last_activity(gateway_id: str, sensor: str):
    redis_key = f"user:{gateway_id}:{sensor}_activity"
    last_activity = r.get(redis_key)
    return {"sensor": sensor, "last_activity": last_activity}

@router.get("/last-activity/{gateway_id}")
async def get_total_activity(gateway_id: str):
    total_activity = r.get(f"user:{gateway_id}:total_activity")
    return {"gateway_id": gateway_id, "total_activity": total_activity}
