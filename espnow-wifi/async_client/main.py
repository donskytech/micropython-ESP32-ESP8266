from espnow_node import EspNowNode
from wifi_node import WiFiNode
import network
import uasyncio as asyncio
from machine import Pin, ADC
import time
import dht
import ujson

MAC = '78:21:84:C6:38:B0'
b_MAC = bytes([int(i, 16) for i in MAC.split(':')])

wifi = WiFiNode()
espnow = EspNowNode(peer_mac=b_MAC)

# Define the GPIO pin to which the PIR sensor is connected (change this as needed)
pir_pin = Pin(36, Pin.IN)

# Define GPIO pin for the DHT sensor
dht_pin = Pin(32)
dht_sensor = dht.DHT22(dht_pin)

ir_pin = Pin(25, Pin.IN)

async def send_pir_motion_readings():
    while True:
        motion_detected = pir_pin.value()

        if motion_detected:
            print("Motion detected!")
            message = {"pir_alert_detected": True}
            await espnow.node.asend(ujson.dumps(message))
        else:
#             print("No motion detected.")
            pass
        await asyncio.sleep_ms(1000)  
        
# Async function for sending DHT temperature data
async def send_dht_temperature_data():
    while True:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        print(f"temperature : {temperature}, humidity: {humidity}")
        message = {"temperature":temperature, "humidity": humidity}
        await espnow.node.asend(ujson.dumps(message))
        await asyncio.sleep(30)
    
async def send_ir_data():
    while True:
        # Read data from the IR sensor
        ir_data = ir_pin.value()
        
        if ir_data == 0:
            print(f"Infrared Alert!")
            message = {"infrared_alert_detected": True}
            await espnow.node.asend(ujson.dumps(message))

        await asyncio.sleep_ms(2000)  
        
async def main():
    await asyncio.gather(send_pir_motion_readings(), send_dht_temperature_data(), send_ir_data())
#     await asyncio.gather(send_pir_motion_readings(), send_ir_data())
        
asyncio.run(main())

