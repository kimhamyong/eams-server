import os
import json
import asyncio
from gmqtt import Client as MQTTClient
from dotenv import load_dotenv
from app.redis import save_activity
from ws.ws_handlers import send_websocket_activity
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

# Load MQTT broker and topic from environment variables
BROKER = os.getenv("MQTT_BROKER")
PORT = int(os.getenv("MQTT_PORT"))
TOPIC = os.getenv("MQTT_TOPIC")

# Initialize MQTT client
mqtt_client = MQTTClient("mqtt_client")

async def on_message(client, topic, payload, qos, properties):
    """Handle incoming MQTT messages."""
    try:
        # Decode and parse the JSON message
        data = json.loads(payload.decode())
        gateway_id = data["gateway_id"]
        sensor = data["sensor"]
        timestamp = data["timestamp"]

        # Store activity data in Redis
        save_activity(gateway_id, sensor, timestamp)

        # Send activity data to WebSocket clients
        activity_data = {
            "gateway_id": gateway_id,
            "sensor": sensor,
            "timestamp": timestamp
        }
        print(f"📩 MQTT Received: {data}")  # Debugging print statement
        asyncio.create_task(send_websocket_activity(activity_data))  # Send via WebSocket asynchronously

    except Exception as e:
        print(f"❌ MQTT Data Processing Error: {e}")  # Debugging error print statement

async def start_mqtt():
    """Establish an MQTT connection and subscribe to the topic."""
    mqtt_client.on_message = on_message  # Set callback function for incoming messages
    await mqtt_client.connect(BROKER, PORT)  # Connect to the MQTT broker
    mqtt_client.subscribe(TOPIC, qos=0)  # Subscribe to the specified topic
    print(f"✅ MQTT connected & subscribed to topic: {TOPIC}")  # Debugging print statement
