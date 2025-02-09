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

# Load MQTT broker and topic information from environment variables
BROKER = os.getenv("MQTT_BROKER")  # MQTT broker address
PORT = int(os.getenv("MQTT_PORT"))  # MQTT broker port
TOPIC = os.getenv("MQTT_TOPIC")  # MQTT topic to subscribe to

# Initialize an MQTT client instance
mqtt_client = MQTTClient("mqtt_client")

async def on_message(client, topic, payload, qos, properties):
    """Processes incoming MQTT messages and handles sensor activity data."""
    try:
        # Decode the received payload and parse it as JSON
        data = json.loads(payload.decode())

        # Extract required fields from the MQTT message
        gateway_id = data["gateway_id"]
        sensor = data["sensor"]
        timestamp = data["timestamp"]

        # Save the last activity timestamp for the given sensor in Redis
        save_activity(gateway_id, sensor, timestamp)

        # Prepare activity data for WebSocket transmission
        activity_data = {
            "gateway_id": gateway_id,
            "sensor": sensor,
            "timestamp": timestamp
        }

        # Debugging print statement to verify received data
        print(f"📩 MQTT Received: {data}")

        # Send the activity data asynchronously to WebSocket clients
        asyncio.create_task(send_websocket_activity(activity_data))

    except Exception as e:
        # Log an error message if MQTT data processing fails
        print(f"❌ MQTT Data Processing Error: {e}")

async def start_mqtt():
    """Establishes an MQTT connection and subscribes to the specified topic."""
    
    # Assign the message handling function to the MQTT client
    mqtt_client.on_message = on_message

    # Connect to the MQTT broker using the provided host and port
    await mqtt_client.connect(BROKER, PORT)

    # Subscribe to the configured topic to receive messages
    mqtt_client.subscribe(TOPIC, qos=0)

    # Debugging print statement to confirm successful connection
    print(f"✅ MQTT connected & subscribed to topic: {TOPIC}")
