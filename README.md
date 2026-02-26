# Full-Stack IoT Telemetry Dashboard

A professional-grade IoT data logging and visualization system. This project demonstrates a complete end-to-end telemetry pipeline, utilizing an ESP32 for edge data collection, MQTT for lightweight messaging, a Python Flask backend for data processing, and MySQL for persistent storage.

## System Architecture
* **Edge Device:** ESP32 (C++/Arduino)
* [cite_start]**Messaging Protocol:** MQTT (Broker: `mqtt.iotbhai.io`) [cite: 3]
* **Backend:** Python (Flask) with `paho-mqtt`
* **Database:** MySQL (`senseHub`)
* **Frontend:** HTML/CSS/JS with Chart.js for real-time visualization

## Key Features
* [cite_start]**Non-Blocking Architecture:** The ESP32 firmware avoids `delay()`, ensuring continuous main loop execution and responsive telemetry[cite: 1].
* [cite_start]**Robust Connectivity:** Features automatic reconnection logic for both WiFi and the MQTT broker[cite: 1].
* [cite_start]**State Monitoring (LWT):** Utilizes MQTT Last Will and Testament (LWT) to track device online/offline status automatically[cite: 1, 19, 20].
* [cite_start]**Bidirectional Communication:** Sends serialized JSON telemetry data [cite: 1] (simulated temperature, humidity, RSSI, and uptime) [cite_start][cite: 29, 30] [cite_start]while actively listening for remote commands to control an onboard LED on Pin 2[cite: 6, 10, 15].
* **Dynamic Frontend:** Real-time web dashboard featuring dynamic Chart.js line graphs with time-based data filtering (Live, 1h, 24h) and asynchronous remote control buttons.

## Prerequisites
* **Hardware:** ESP32 development board.
* [cite_start]**C++ Libraries:** `WiFi`, `PubSubClient`, and `ArduinoJson` (v7)[cite: 1, 28].
* **Python Packages:** `flask`, `mysql-connector-python`, `paho-mqtt`.
* **Database:** A local MySQL server instance.

## Installation & Setup

### 1. Database Initialization
Create a MySQL database named `senseHub` and create a table to store the incoming data. 
*(Note: Ensure your MySQL credentials match `tiputheadmin` / `tipu_1234` or update `app.py` accordingly).*

### 2. Backend Configuration
1. Navigate to your Python backend directory.
2. Install the required dependencies:
   ```bash
   pip install flask mysql-connector-python paho-mqtt
