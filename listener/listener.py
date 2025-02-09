import asyncio
from listener.subscriber import start_subscriber
from listener.publisher import start_publisher

async def start_listener():
    """Starts both the Redis Subscriber and Publisher asynchronously.

    - Runs `start_subscriber()` to listen for alerts from Redis Pub/Sub.
    - Runs `start_publisher()` to detect key expirations in Redis.
    - Uses `asyncio.create_task()` to prevent blocking the FastAPI event loop.
    """
    print("🚀 Redis Listener Started!")

    # Run both the subscriber and publisher as independent async tasks
    asyncio.create_task(start_subscriber())  
    asyncio.create_task(start_publisher())  
