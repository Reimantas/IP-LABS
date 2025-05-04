import paho.mqtt.client as mqtt
from weather import weather_search
import webbrowser
import json

MQTT_TOPIC = "expo/test"
MQTT_BROKER = "172.20.10.3"
MQTT_PORT = 1883  

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, message):
    city = str(message.payload.decode("utf-8")).strip()
    print(f"Received city query: {city}")
    if city:
        # Get weather data
        content = weather_search(city)
        print(f"Weather result: {content}")
        
        # Open browser with weather page (if no error)
        if "web_url" in content:
            webbrowser.open(content["web_url"])
        
        # Publish result back to EXPO
        client.publish("expo/status", json.dumps(content))

# Initialize MQTT client
client = mqtt.Client(client_id="WeatherSubscriber", protocol=mqtt.MQTTv311)

# Set callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT)
except Exception as e:
    print(f"Failed to connect to broker: {e}")
    exit(1)

# Start the loop
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Shutting down...")
    client.disconnect()