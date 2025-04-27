import paho.mqtt.client as mqtt
import time

def connect_broker(broker_address, client_name):
    client = mqtt.Client(client_id=client_name, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
    client.connect(broker_address)
    time.sleep(1)
    client.loop_start()
    return client

if __name__ == "__main__":
    server = "broker.hivemq.com"
    client_name = "tester"
    client = connect_broker(server, client_name)
    
    try:
        while True:
            message = input('Send some random message: ')
            client.publish("temperature", message)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()