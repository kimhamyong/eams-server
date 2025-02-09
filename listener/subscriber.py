import asyncio
import redis
from ws.ws_handlers import send_websocket_alert
import os
from dotenv import load_dotenv

load_dotenv()

# Load Redis host and port from environment variables
REDIS_HOST = os.getenv("REDIS_HOST")  # Default set to 'redis'
REDIS_PORT = int(os.getenv("REDIS_PORT"))  # Redis port number

def get_redis_client():
    """Returns a Redis client instance."""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def subscribe_alerts():
    """Subscribes asynchronously to the Redis Pub/Sub `alert_channel`.

    - Listens for messages on `alert_channel` where expired gateway data triggers an alert.
    - If no remaining data exists for a gateway, a WebSocket alert is sent.
    """
    r = get_redis_client()
    pubsub = r.pubsub()
    pubsub.subscribe("alert_channel")

    print("📡 Subscribing to alert_channel...")

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message:
            gateway_id = message["data"]
            
            # Check if there is any remaining data for the gateway in Redis
            remaining_keys = r.keys(f"{gateway_id}:*")
            
            if not remaining_keys:  # Only send a WebSocket alert if all data is deleted
                alert_data = {
                    "gateway_id": gateway_id,
                    "message": "no activity detected"
                }
                await send_websocket_alert(alert_data)
                print(f"🚨 Sent WebSocket Alert: {alert_data}")
            else:
                print(f"⏳ Alert received but data still exists for {gateway_id}, skipping alert.")
        
        await asyncio.sleep(0.1)  # Prevents high CPU usage by adding a small delay

async def start_subscriber():
    """Starts the Redis subscriber as an independent async task."""
    asyncio.create_task(subscribe_alerts())  # Runs independently without blocking FastAPI
