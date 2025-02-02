from fastapi import FastAPI
import asyncio
from app.routers import redis_activity, send_activity
from ws.websocket_server import websocket_endpoint  # ✅ WebSocket 엔드포인트 추가
from mqtt.mqtt_handler import start_mqtt

# FastAPI 애플리케이션 생성
app = FastAPI()

# 라우터 추가 (API 엔드포인트)
app.include_router(redis_activity.router, tags=["redis_activity"])
app.include_router(send_activity.router, tags=["send_activity"])

# ✅ WebSocket 엔드포인트 등록
app.add_api_websocket_route("/ws", websocket_endpoint)  # ✅ 추가!

# MQTT 백그라운드 작업 실행
@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI 서버 시작됨!")
    asyncio.create_task(start_mqtt())  # ✅ MQTT 실행

# 기본 라우트
@app.get("/")
async def read_root():
    return {"message": "Server is running"}