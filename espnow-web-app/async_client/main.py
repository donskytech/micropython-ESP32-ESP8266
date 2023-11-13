from espnow_node import EspNowNode
from wifi_node import WiFiNode
import network
import uasyncio as asyncio
from machine import Pin, ADC
import time
import dht
import ujson
from soil_moisture_sensor_module import SoilMonitor

MAC = '24:DC:C3:AF:C1:F8'
b_MAC = bytes([int(i, 16) for i in MAC.split(':')])

# wifi = WiFiNode()
espnow = EspNowNode(peer_mac=b_MAC)

soil_monitor_module = SoilMonitor()

async def send_soil_moisture_readings():
    while True:
        message = soil_monitor_module.read_soil_moisture()
        print(f'Sending Soil Moisture sensor: {message}')
        await espnow.node.asend(ujson.dumps(message))

        await asyncio.sleep_ms(5000) 

 
        
async def main():
    await asyncio.gather(send_soil_moisture_readings())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Interrupted')
finally:
    asyncio.new_event_loop()

