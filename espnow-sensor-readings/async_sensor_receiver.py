import network
import aioespnow
from machine import I2C, Pin
import asyncio
import ujson
from lcd_i2c import LCD

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# Initialize ESP-NOW
esp = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
esp.active(True)

pir_pin = Pin(32, Pin.OUT)
infrared_pin = Pin(23, Pin.OUT)
buzzer_pin = Pin(19, Pin.OUT)

I2C_ADDR = 0x27     # DEC 39, HEX 0x27
NUM_ROWS = 2
NUM_COLS = 16

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=10000)
lcd = LCD(addr=I2C_ADDR, cols=NUM_COLS, rows=NUM_ROWS, i2c=i2c)

lcd.begin()

async def trigger_pir_alert():
    pir_pin.on()
    await asyncio.sleep(1)
    pir_pin.off()
    
async def trigger_infrared_alert():
    infrared_pin.on()
    buzzer_pin.value(1)
    await asyncio.sleep(1)
    infrared_pin.off()
    buzzer_pin.value(0)
    
async def display_temperature(temp):
    lcd.set_cursor(col=0, row=0)
    lcd.print(f"Temp: {temp} C")
    
async def display_humidity(humidity):
    lcd.set_cursor(col=0, row=1)
    lcd.print(f"Humidity: {humidity} %")

async def wait_for_message():
    while True:
        _, msg = esp.recv()
        if msg:             # msg == None if timeout in recv()
            msg = ujson.loads(msg)
            print(msg)
            if "pir_alert_detected" in msg:
                await trigger_pir_alert()
            elif "infrared_alert_detected" in msg:
                await trigger_infrared_alert()
            elif "temperature"  in msg:
                await display_temperature(msg['temperature'])
            elif "humidity" in msg:
                await display_humidity(msg['humidity'])
            

asyncio.run(wait_for_message())


