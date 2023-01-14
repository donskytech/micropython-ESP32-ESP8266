import time
import ubinascii
import machine
from umqtt.simple import MQTTClient
from machine import Pin

# Default MQTT server to connect to
SERVER = "192.168.100.22"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"temperature"


def main():
    mqttClient = MQTTClient(CLIENT_ID, SERVER, keepalive=60)
    mqttClient.connect()
    print(f"Connected to MQTT  Broker :: {SERVER}")

    mqttClient.publish(TOPIC, b"49")
    mqttClient.disconnect()
    
if __name__ == "__main__":
    main()

