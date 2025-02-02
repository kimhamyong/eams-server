from fastapi import FastAPI
import asyncio
from app.routers import redis_activity, send_activity, send_alert
from ws.websocket_server import websocket_endpoint  
from mqtt.mqtt_handler import start_mqtt

from fastapi.middleware.cors import CORSMiddleware

# FastAPI 애플리케이션 생성
app = FastAPI()

# ✅ CORS 미들웨어 추가 (모든 출처 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (보안이 필요한 경우 특정 도메인만 허용 가능)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST 등)
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)


# 라우터 추가 (API 엔드포인트)
app.include_router(redis_activity.router, tags=["redis_activity"])
app.include_router(send_activity.router, tags=["send_activity"])
app.include_router(send_alert.router, tags=["send_alert"])

# ✅ WebSocket 엔드포인트 등록
app.add_api_websocket_route("/ws", websocket_endpoint) 

# MQTT 백그라운드 작업 실행
@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI 서버 시작됨!")
    asyncio.create_task(start_mqtt())

# 기본 라우트
@app.get("/")
async def read_root():
    return {"message": "Server is running"}
