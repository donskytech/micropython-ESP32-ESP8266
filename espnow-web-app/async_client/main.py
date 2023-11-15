from espnow_node import EspNowNode
from wifi_node import WiFiNode
import network
import uasyncio as asyncio
from machine import Pin, ADC
import time
import dht
import ujson
from soil_moisture_sensor_module import SoilMonitor
import config
import urandom

MAC = '24:DC:C3:AF:C1:F9'
b_MAC = bytes([int(i, 16) for i in MAC.split(':')])

wifi = WiFiNode()
# A WLAN interface must be active to send()/recv()
network.WLAN(network.STA_IF).active(True)
espnow = EspNowNode(peer_mac=b_MAC)

soil_monitor_module = SoilMonitor()

def generate_random_number(start, end):
    return urandom.randint(start, end)

async def send_soil_moisture_readings():
    while True:
#         message = {"soil_monitor": config.SOIL_MONITOR_MODULE_1, "sensor_reading": soil_monitor_module.read_soil_moisture()}
        message = {"soil_monitor_id": config.SOIL_MONITOR_ID, "soil_monitor": config.SOIL_MONITOR_MODULE_1, "sensor_reading": generate_random_number(5000, 65000)} 
        print(f'Sending Soil Moisture sensor: {message}')
        await espnow.node.asend(ujson.dumps(message))
        
        await asyncio.sleep_ms(2000)

async def main():
    await asyncio.gather(send_soil_moisture_readings())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Interrupted')
finally:
    asyncio.new_event_loop()

