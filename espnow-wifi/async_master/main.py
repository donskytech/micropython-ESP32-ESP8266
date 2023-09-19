from espnow_node import EspNowNode
from wifi_node import WiFiNode
import uasyncio as asyncio
from mqtt_as import MQTTClient, config
import wifi_config
import network
import aioespnow
from machine import I2C, Pin
import ujson
from lcd_i2c import LCD

MAC_0 = 'C8:F0:9E:0D:B6:04'
b_MAC = [bytes([int(i, 16) for i in mac.split(':')]) for mac in [MAC_0]]

config['ssid'] = wifi_config.SSID  # Optional on ESP8266
config['wifi_pw'] = wifi_config.PASSWORD
config['server'] = '192.168.100.22'  # Change to suit your setup
config["queue_len"] = 1  # Use event interface with default queue size

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
espnow = EspNowNode(peers_mac=b_MAC)
wifi = WiFiNode(wifi_config.SSID, wifi_config.PASSWORD)

pir_pin = Pin(32, Pin.OUT)
infrared_pin = Pin(23, Pin.OUT)
buzzer_pin = Pin(19, Pin.OUT)

I2C_ADDR = 0x27     # DEC 39, HEX 0x27
NUM_ROWS = 2
NUM_COLS = 16

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)
lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)

lcd.begin()


async def trigger_pir_alert(msg):
    pir_pin.on()
    await client.publish("alert", ujson.dumps(msg), qos = 1)
    await asyncio.sleep(1)
    pir_pin.off()
    
async def trigger_infrared_alert(msg):
    infrared_pin.on()
    buzzer_pin.value(1)
    await client.publish("alert", ujson.dumps(msg), qos = 1)
    await asyncio.sleep(1)
    infrared_pin.off()
    buzzer_pin.value(0)
    
async def display_temp_humidity(msg):
    temperature = msg['temperature']
    lcd.set_cursor(col=0, row=0)
    lcd.print(f"Temp: {temperature} C")
    humidity = msg['humidity']
    lcd.set_cursor(col=0, row=1)
    lcd.print(f"Humidity: {humidity} %")
    await client.publish("alert", ujson.dumps(msg), qos = 1)
    await asyncio.sleep(1)
    
async def display_humidity(msg):
    humidity = msg['humidity']
    lcd.set_cursor(col=0, row=1)
    lcd.print(f"Humidity: {humidity} %")
    await client.publish("alert", ujson.dumps(msg), qos = 1)
    await asyncio.sleep(1)


async def messages(client):  # Respond to incoming messages
    async for topic, msg, retained in client.queue:
        print((topic, msg, retained))

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
#         await client.subscribe('foo_topic', 1)  # renew subscriptions
        
async def wait_for_message():
    async for mac, msg in espnow.node:
        if msg:
            try:
                msg = ujson.loads(msg)    
            except ValueError as e:
                print(f"Parsing Error: {e}")
            else:                
                print(msg)
                if "pir_alert_detected" in msg:
                    await trigger_pir_alert(msg)
                elif "infrared_alert_detected" in msg:
                    await trigger_infrared_alert(msg)
                elif "temperature"  in msg:
                    await display_temp_humidity(msg)

async def recv_cb():
    while True:  # Read out all messages waiting in the buffer
        msg = espnow.node.airecv()  # Don't wait if no messages left
        if msg is None:
            return
        
        for val in msg:
            print(val)


async def main():
    print("MQTT Connect in progress...")
    await client.connect()
    print("Sleep for some time...")
    await asyncio.sleep(3)
    print("Creating task....")

    await asyncio.gather( wait_for_message(), messages(client), up(client))
    
asyncio.run(main())
