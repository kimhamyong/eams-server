from fastapi import FastAPI
import asyncio
from gmqtt import Client as MQTTClient
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

# hiveMQ Cloud 브로커 사용
BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
USERNAME = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")

# FastAPI 애플리케이션 생성
app = FastAPI()

# TLS/SSL 설정 (hiveMQ Cloud)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.load_default_certs()

# MQTT 클라이언트 생성
mqtt_client = MQTTClient("client")

# HiveMQ Cloud 인증 추가
mqtt_client.set_auth_credentials(USERNAME, PASSWORD)

# MQTT 메시지를 처리하는 콜백 함수
def on_message(client, topic, payload, qos, properties):
    print(f"📩 Received message: {payload.decode()} on topic: {topic}")

# MQTT 클라이언트 설정
mqtt_client.on_message = on_message

# MQTT 연결 및 구독 설정 (TLS 사용)
async def connect_and_subscribe():
    try:
        print(f"🚀 MQTT 클라이언트 연결 시도... (Broker: {BROKER}, Port: {PORT})")
        await mqtt_client.connect(BROKER, port=PORT, ssl=ssl_context)  # ✅ TLS 적용
        mqtt_client.subscribe("test", qos=0)  # 구독할 토픽
        print("✅ MQTT client connected and subscribed")
    except Exception as e:
        print(f"❌ MQTT 연결 실패: {e}")

# FastAPI 이벤트: 애플리케이션 시작 시 MQTT 클라이언트 연결
@app.on_event("startup")
async def startup_event():
    print("🚀 FastAPI 서버 시작됨!")
    asyncio.create_task(connect_and_subscribe())

# FastAPI 이벤트: 애플리케이션 종료 시 MQTT 클라이언트 연결 해제
@app.on_event("shutdown")
async def shutdown_event():
    await mqtt_client.disconnect()

# HTTP 라우트 예시
@app.get("/")
async def read_root():
    return {"message": "MQTT Subscriber is running"}
