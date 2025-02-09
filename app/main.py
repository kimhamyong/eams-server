from fastapi import FastAPI
import asyncio
from app.routers import router
from ws.ws_server import websocket_endpoint  
from mqtt.mqtt_handler import start_mqtt
from listener.listener import start_listener

app = FastAPI() 

app.include_router(router, tags=["routers"])
app.add_api_websocket_route("/ws", websocket_endpoint) 

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_mqtt())   
    asyncio.create_task(start_listener())
