import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

# Set TTL (Time To Live) for stored data - 24 hours (86400 seconds)
TTL = 8

# Global Redis client (Created once and reused to avoid unnecessary connections)
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def save_activity(gateway_id: str, sensor: str, timestamp: str):
    """Save the last detected time of a sensor and delete it automatically after 24 hours."""
    
    # Generate a unique key for the sensor activity
    redis_key = f"{gateway_id}:{sensor}_activity"

    # Store the last detection time for a specific sensor with an expiration time
    redis_client.set(redis_key, timestamp)
    redis_client.expire(redis_key, TTL)  

    # Store the most recent activity timestamp across all sensors for this gateway
    total_activity_key = f"{gateway_id}:total_activity"
    redis_client.set(total_activity_key, timestamp)
    redis_client.expire(total_activity_key, TTL)  

def get_last_activity(gateway_id: str, sensor: str):
    """Retrieve the last detected time for a specific sensor in the given gateway."""
    
    # Generate the key for retrieving sensor-specific activity
    redis_key = f"{gateway_id}:{sensor}_activity"
    return redis_client.get(redis_key)

def get_total_activity(gateway_id: str):
    """Retrieve the last detected time across all sensors for the given gateway."""
    
    # Retrieve the latest recorded activity across all sensors
    return redis_client.get(f"{gateway_id}:total_activity")
