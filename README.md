# Full-Stack IoT Telemetry Dashboard

A professional-grade IoT data logging and visualization system. This project demonstrates a complete end-to-end telemetry pipeline, utilizing an ESP32 for edge data collection, MQTT for lightweight messaging, a Python Flask backend for data processing, and MySQL for persistent storage.

## System Architecture
* **Edge Device:** ESP32 (C++/Arduino)
* **Messaging Protocol:** MQTT (Broker: `mqtt.iotbhai.io`)
* **Backend:** Python (Flask) with `paho-mqtt`
* **Database:** MySQL (`senseHub`)
* **Frontend:** HTML/CSS/JS with Chart.js for real-time visualization

## Key Features
* **Non-Blocking Architecture:** The ESP32 firmware avoids `delay()`, ensuring continuous main loop execution and responsive telemetry.
* **Robust Connectivity:** Features automatic reconnection logic for both WiFi and the MQTT broker.
* **State Monitoring (LWT):** Utilizes MQTT Last Will and Testament (LWT) to track device online/offline status automatically.
* **Bidirectional Communication:** Sends serialized JSON telemetry data while actively listening for remote commands to control an onboard LED on Pin 2.
* **Dynamic Frontend:** Real-time web dashboard featuring dynamic Chart.js line graphs with time-based data filtering (Live, 1h, 24h) and asynchronous remote control buttons.

## Prerequisites
* **Hardware:** ESP32 development board.
* **C++ Libraries:** `WiFi`, `PubSubClient`, and `ArduinoJson` (v7).
* **Python Packages:** `flask`, `mysql-connector-python`, `paho-mqtt`.
* **Database:** A local MySQL server instance.

## Installation & Setup

### 1. Database Initialization
Create a MySQL database named `senseHub` and execute the following SQL to create the required table for the telemetry data:

```sql
CREATE DATABASE IF NOT EXISTS senseHub;
USE senseHub;

CREATE TABLE IF NOT EXISTS mqtt_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    device_id VARCHAR(50),
    temperature FLOAT,
    humidity FLOAT,
    uptime INT,
    rssi INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
### 2. Backend Configuration
1. Navigate to your Python backend directory.
2. Install the required dependencies:
   ```bash
   pip install flask mysql-connector-python paho-mqtt
   ```
   
### 3. Update app.py with your MySQL credentials 
```python
db_config = {
    'host': 'localhost',
    'user': 'tiputheadmin',          
    'password': 'tipu_1234',  
    'database': 'senseHub'
}
```

### 4. Run the Flask application:
``` bash
    python app.py
```
The dashboard will be available at http://localhost:5000.
### 5. ESP32 Firmware Flashing
1. Open `Build_a_Full_Stack_IoT_Dashboard.ino` in your Arduino IDE or PlatformIO.
2. Update the WiFi configuration:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID"; 
   const char* password = "YOUR_WIFI_PASSWORD";
   ```
3. Verify the MQTT broker settings (defaults to mqtt.iotbhai.io on port 1883).
4. Compile and upload to your ESP32 board.
