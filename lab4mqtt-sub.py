import paho.mqtt.client as mqtt
import json
from linux import get_directory_contents, get_ip_addresses, get_free_memory, create_file

# MQTT brokerio nustatymai
MQTT_BROKER = "172.20.10.2"  # Mosquitto brokerio adresas Linux serveryje
MQTT_PORT = 1883
MQTT_TOPIC_SUB = "expo/test"
MQTT_TOPIC_PUB = "expo/status"

# Callback funkcija, kai prisijungiama prie brokerio
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"Prisijungta prie MQTT brokerio su kodu {reason_code}")
        client.subscribe(MQTT_TOPIC_SUB)
    else:
        print(f"Prisijungimo klaida, kodas: {reason_code}")

# Callback funkcija, kai gaunama žinutė
def on_message(client, userdata, msg):
    try:
        command = msg.payload.decode("utf-8").strip().lower()
        print(f"Gauta komanda: {command}")

        # Vykdomos atitinkamos funkcijos pagal komandą
        if command == "directory":
            result = get_directory_contents()
            client.publish(MQTT_TOPIC_PUB, json.dumps({"action": "directory_contents", "result": result}))
        elif command == "ip":
            result = get_ip_addresses()
            client.publish(MQTT_TOPIC_PUB, json.dumps({"action": "ip_addresses", "result": result}))
        elif command == "memory":
            result = get_free_memory()
            client.publish(MQTT_TOPIC_PUB, json.dumps({"action": "free_memory", "result": result}))
        elif command == "create_file":
            result = create_file()
            client.publish(MQTT_TOPIC_PUB, json.dumps({"action": "file_created", "result": result}))
        else:
            client.publish(MQTT_TOPIC_PUB, json.dumps({"action": command, "error": "Neteisinga komanda"}))
    except Exception as e:
        client.publish(MQTT_TOPIC_PUB, json.dumps({"error": str(e)}))

# Pagrindinė funkcija
def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="LinuxSubscriber", protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    client.on_message = on_message

    # Prisijungimas prie brokerio
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
    except Exception as e:
        print(f"Nepavyko prisijungti prie brokerio: {e}")
        exit(1)

    # Amžinas ciklas, kad programa veiktų
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Programa uždaroma...")
        client.disconnect()

if __name__ == "__main__":
    main()