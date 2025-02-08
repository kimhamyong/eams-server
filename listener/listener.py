import asyncio
from listener.subscriber import start_subscriber
from listener.publisher import start_publisher

async def start_listener():
    """Subscriber 및 Publisher 실행 (비동기 실행)"""
    print("🚀 Redis Listener Started!")

    # ✅ 비동기 실행 (FastAPI 블로킹 방지)
    asyncio.create_task(start_subscriber())  
    asyncio.create_task(start_publisher())
