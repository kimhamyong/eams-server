import redis
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Load Redis host and port from environment variables
REDIS_HOST = os.getenv("REDIS_HOST")  # Default set to 'redis'
REDIS_PORT = int(os.getenv("REDIS_PORT"))  # Redis port number

def get_redis_client():
    """Returns a Redis client instance."""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def redis_expire_listener():
    """Monitors expired keys in Redis and publishes alerts when necessary.

    - Listens for Redis key expiration events (`__keyevent@0__:expired`).
    - When `total_activity` key expires, it checks if all related data is removed.
    - If no data remains for the gateway, it publishes an alert to `alert_channel`.
    """
    r = get_redis_client()
    pubsub = r.pubsub()
    pubsub.psubscribe("__keyevent@0__:expired")

    print("📡 Listening for expired keys...")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message and message["type"] == "pmessage":
            expired_key = message["data"]

            # Extract gateway ID (e.g., home1:total_activity → home1)
            if expired_key.endswith(":total_activity"):
                gateway_id = expired_key.split(":")[0]

                # Wait 1 second after TTL expiration before checking Redis
                await asyncio.sleep(1.0)

                # Check if any data remains for the expired gateway
                remaining_keys = r.keys(f"{gateway_id}:*")

                if not remaining_keys:  # Only publish an alert if all data is removed
                    r.publish("alert_channel", gateway_id)
                    print(f"📢 Published Alert for Gateway: {gateway_id}")
                else:
                    print(f"⏳ TTL expired but {gateway_id} still has data: {remaining_keys}")
        
        await asyncio.sleep(0.1)  # Prevent event loop blocking

async def start_publisher():
    """Starts the Redis expiration event listener in an asynchronous task."""
    asyncio.create_task(redis_expire_listener())  # Run independently
