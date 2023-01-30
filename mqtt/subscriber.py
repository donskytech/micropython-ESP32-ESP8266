import time
import ubinascii
from umqtt.simple import MQTTClient
import machine

# Default MQTT MQTT_BROKER to connect to
MQTT_BROKER = "192.168.100.22"
CLIENT_ID = ubinascii.hexlify(machine.unique_id())
TOPIC = b"temperature"

# Ping the MQTT broker since we are not publishing any message
last_ping = time.time()
ping_interval = 60

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))


def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()
    
def main():
    mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=60)
    mqttClient.set_callback(sub_cb)
    mqttClient.connect()
    mqttClient.subscribe(TOPIC)
    print(f"Connected to MQTT  Broker :: {MQTT_BROKER}, and waiting for callback function to be called!")
    while True:
        if False:
            # Blocking wait for message
            mqttClient.wait_msg()
        else:
            # Non-blocking wait for message
            mqttClient.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            global last_ping
            if (time.time() - last_ping) >= ping_interval:
                mqttClient.ping()
                last_ping = time.time()
                now = time.localtime()
                print(f"Pinging MQTT Broker, last ping :: {now[0]}/{now[1]}/{now[2]} {now[3]}:{now[4]}:{now[5]}")
            time.sleep(1)
            
    print("Disconnecting...")
    mqttClient.disconnect()


if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print("Error: " + str(e))
        reset()
