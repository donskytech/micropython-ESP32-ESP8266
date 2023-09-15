import network
import aioespnow
import asyncio
from machine import Pin, ADC
import time
import dht
import ujson

# A WLAN interface must be active to send()/recv()
network.WLAN(network.STA_IF).active(True)

esp = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
esp.active(True)
peer = b'x!\x84\xc68\xb0'
esp.add_peer(peer)

# Define the GPIO pin to which the PIR sensor is connected (change this as needed)
pir_pin = Pin(36, Pin.IN)

# Define GPIO pin for the DHT sensor
dht_pin = Pin(32)
dht_sensor = dht.DHT22(dht_pin)

ir_pin = Pin(25, Pin.IN)

async def send_pir_motion_readings(espnow):
    while True:
        motion_detected = pir_pin.value()

        if motion_detected:
            print("Motion detected!")
            message = {"pir_alert_detected": True}
            await espnow.asend(peer, ujson.dumps(message))
        else:
#             print("No motion detected.")
            pass
        await asyncio.sleep_ms(1000)  
        
# Async function for sending DHT temperature data
async def send_dht_temperature_data(espnow):
    while True:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        print(f"temperature : {temperature}, humidity: {humidity}")
        message = {"temperature":temperature}
        await espnow.asend(peer, ujson.dumps(message))
        message = {"humidity":humidity}
        await espnow.asend(peer, ujson.dumps(message))
        await asyncio.sleep(3)  
    
async def send_ir_data(espnow):
    while True:
        # Read data from the IR sensor
        ir_data = ir_pin.value()
#         print(f"Infrared Value : {ir_data}")
        
        if ir_data == 0:
            print(f"Infrared Alert!")
            message = {"infrared_alert_detected": True}
            await espnow.asend(peer, ujson.dumps(message))

        await asyncio.sleep_ms(500)  
        
async def main(espnow):
    await asyncio.gather(send_pir_motion_readings(espnow), send_dht_temperature_data(espnow), send_ir_data(espnow))
        
        
asyncio.run(main(esp))

