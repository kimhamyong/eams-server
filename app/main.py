from fastapi import FastAPI
import asyncio
from app.mqtt_handler import start_mqtt
from app.routers import redis_activity

# FastAPI 애플리케이션 생성
app = FastAPI()

app.include_router(redis_activity.router, tags=["redis_activity"])

# MQTT 백그라운드 작업 실행
@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI 서버 시작됨!")
    asyncio.create_task(start_mqtt())

# 기본 라우트
@app.get("/")
async def read_root():
    return {"Server is running"}