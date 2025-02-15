# Elderly Activity Monitoring System
This project aims to prevent lonely deaths among elderly individuals living alone by providing a privacy-friendly home monitoring solution. Unlike traditional monitoring systems, this approach does not use cameras or wearable devices, ensuring a non-intrusive and respectful solution for elderly care.
The system utilizes various sensors to track motion and activity patterns, transmitting data via a home gateway. If prolonged inactivity is detected, a warning message is sent to caregivers via the user interface.

**This project is divided into multiple repositories:**  
[Click Details] -> **[End-Node](https://github.com/kimhamyong/eams-node)**, **[Home-Gateway](https://github.com/kimhamyong/eams-gateway)**, **[Server](https://github.com/kimhamyong/eams-server)**

```   
 ┌──────────────┐           ┌──────────────────┐           ┌────────────┐           ┌────────┐
 │   End Node   │     →     │   Home Gateway   │     →     │   Server   │     →     │   UI   │
 └──────────────┘           │         │        │           └────────────┘           └────────┘
                   (ZigBee) │         │        │   (MQTT)                (WebSocket)
                            │    MQTT Broker   │
                            └──────────────────┘  
```

## Overview
This repository contains the **server application**, responsible for handling real-time sensor data.  
- Subscribes to **MQTT messages** from Home-Gateways (`{prefix}/{number}` topic).  
- Updates **in real-time via WebSockets** when new data is received.  
- When **TTL expires, Redis publishes an expiration event**, prompting the server to check for user activity.  
  If no activity is detected across the entire gateway, a **warning message is sent to the UI**.  


## Environment
The server runs in a **containerized environment** using **Docker & Docker Compose**, managing multiple services including **FastAPI** and **Redis**. All dependencies are listed in `requirements.txt` and installed within the containers.


## File Structure
```
server/
│── app/
│   ├── main.py         # Entry point for FastAPI server  
│   ├── redis.py        # Manages Redis-based activity tracking  
│   ├── routers.py      # Defines API routes  
│── listener/
│   ├── listener.py     # Detects Redis TTL expiration events  
│   ├── publisher.py    # Publishes data via Redis Pub/Sub  
│   ├── subscriber.py   # Subscribes to Redis Pub/Sub events  
│── mqtt/
│   ├── mqtt_handler.py # Handles incoming MQTT messages  
│── ws/
│   ├── ws_handlers.py  # WebSocket event handling  
│   ├── ws_server.py    # WebSocket server initialization  
│── .env                # Environment variable definitions  
│── .gitignore          # Specifies ignored files for Git  
│── docker-compose.yml  # Defines Docker container services  
│── Dockerfile          # Docker image build configuration  
│── README.md           # Project documentation (this file)  
│── requirements.txt    # Python package dependencies  
```


## Sequence Diagram
```mermaid
sequenceDiagram
    participant MQTT Broker
    participant FastAPI Server
    participant Redis
    participant UI

    MQTT Broker->>FastAPI Server: Forward MQTT message
    activate FastAPI Server
    FastAPI Server->>UI: Send real-time status update
    FastAPI Server->>Redis: Store sensor activity
    deactivate FastAPI Server

    activate Redis
    note over Redis: Data stored with TTL

    Redis->>FastAPI Server: Notify when TTL expires
    deactivate Redis

    activate FastAPI Server
    FastAPI Server->>Redis: Check if all activity exists for a given gateway

    alt If no activity
        FastAPI Server->>UI: Send inactivity warning
    end
    deactivate FastAPI Server
```


## Getting Started
Clone the repository 
```bash
git clone <REPO_URL>
cd <REPO_NAME>
cd server
```
Set up `.env` file
```bash
$ cp .env.example .env
```
Build & run using Docker Compose
```bash
docker compose up --build
```

