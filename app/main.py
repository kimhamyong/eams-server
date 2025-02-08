from fastapi import FastAPI
import asyncio
from app.routers import router
from ws.ws_server import websocket_endpoint  
from mqtt.mqtt_handler import start_mqtt
from listener.listener import start_listener

# FastAPI 애플리케이션 생성
app = FastAPI() 

# 라우터 추가 (API 엔드포인트)
app.include_router(router, tags=["routers"])

# ✅ WebSocket 엔드포인트 등록
app.add_api_websocket_route("/ws", websocket_endpoint) 

# MQTT 백그라운드 작업 실행
@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI 서버 시작됨!")
    asyncio.create_task(start_mqtt())   
    asyncio.create_task(start_listener())

# 기본 라우트
@app.get("/")
async def read_root():
    return {"message": "Server is running"}
