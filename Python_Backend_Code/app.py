from flask import Flask, jsonify, render_template, request
import mysql.connector
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

# --- MySQL Configuration ---
db_config = {
    'host': 'localhost',
    'user': 'tiputheadmin',          
    'password': 'tipu_1234',  
    'database': 'senseHub'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# --- MQTT Configuration ---
# Ensure this matches your ESP32 broker IP
MQTT_BROKER = "mqtt.iotbhai.io" 
MQTT_PORT = 1883
TOPIC_TELEMETRY = "esp32/01/data"
TOPIC_COMMAND = "esp32/01/cmd"

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with code {rc}")
    client.subscribe(TOPIC_TELEMETRY)

def on_message(client, userdata, msg):
    try:
        # Parse the JSON payload from your ESP32
        payload = json.loads(msg.payload.decode('utf-8'))
        
        # Check if this message contains sensor data
        if "temp" in payload:
            device = payload.get("device")
            temp = payload.get("temp")
            hum = payload.get("hum")
            uptime = payload.get("uptime")
            rssi = payload.get("wifi_rssi")

            # Save to database
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO mqtt_data (device_id, temperature, humidity, uptime, rssi) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (device, temp, hum, uptime, rssi))
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Saved: Temp {temp}°C, Hum {hum}% from {device}")
            
        # Check if this message is just the LED confirmation
        elif "led" in payload:
            led_state = payload.get("led")
            print(f"Device confirmed LED state is now: {led_state}")
            # We purposely DO NOT save this to the sensor database table!

    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# Initialize and start MQTT in a background thread
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start() 

# --- Flask Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_data', methods=['GET'])
def get_data():
    # Get the time range from the AJAX request (defaults to 'live')
    time_range = request.args.get('range', 'live')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Dynamically adjust the SQL query based on the filter
    if time_range == '1h':
        # Get all data from the last hour
        query = "SELECT * FROM mqtt_data WHERE timestamp >= NOW() - INTERVAL 1 HOUR ORDER BY timestamp DESC"
    elif time_range == '24h':
        # Get data from the last 24 hours (Limited to 500 points to prevent browser lag)
        query = "SELECT * FROM mqtt_data WHERE timestamp >= NOW() - INTERVAL 24 HOUR ORDER BY timestamp DESC LIMIT 500"
    else:
        # Default 'live' view: Get the last 30 readings
        query = "SELECT * FROM mqtt_data ORDER BY timestamp DESC LIMIT 30"
        
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Reverse to show chronological order on the chart (left to right)
    rows.reverse()
    return jsonify(rows)

# New route to handle button clicks from the dashboard
@app.route('/api/led', methods=['POST'])
def control_led():
    data = request.get_json()
    command = data.get('command')
    
    if command in ["ON", "OFF"]:
        # Publish the command back to the ESP32
        mqtt_client.publish(TOPIC_COMMAND, command)
        return jsonify({"message": f"Sent {command} to ESP32!"}), 200
    
    return jsonify({"error": "Invalid command"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)