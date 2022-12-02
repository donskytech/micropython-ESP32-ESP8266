from machine import Pin
from time import sleep
import dht 
 
dht_sensor = dht.DHT11(Pin(22))
 
while True:
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        print(f"Temperature: {temperature:.2f}")
        print(f"Humidity: {humidity:.2f}")
        sleep(2)
    except OSError as e:
        print(e)
        print('dht_sensor Reading Failed')
