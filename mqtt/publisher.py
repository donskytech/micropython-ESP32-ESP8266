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
    c = MQTTClient(CLIENT_ID, SERVER, keepalive=60)
    c.connect()
    print(f"Connected to MQTT  Broker :: {SERVER}")

    c.publish(TOPIC, b"49")
    c.disconnect()
    
if __name__ == "__main__":
    main()
