import network
import aioespnow
import asyncio
from machine import Pin, ADC

# A WLAN interface must be active to send()/recv()
network.WLAN(network.STA_IF).active(True)

esp = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
esp.active(True)
peer = b'x!\x84\xc68\xb0'
esp.add_peer(peer)

# Create a function to send data when a button is pressed (optional)
button_pin = Pin(32, Pin.IN, Pin.PULL_UP)
debounce_delay = 50  # Adjust this value to your needs (milliseconds)

# Define GPIO pin for the potentiometer
potentiometer_pin = 36
adc = ADC(Pin(potentiometer_pin), atten=ADC.ATTN_11DB)


async def send_button_state(espnow):
    last_state = button_pin.value()
    while True:
        state = button_pin.value()
        if state != last_state:
            await asyncio.sleep_ms(debounce_delay)
            state = button_pin.value()
            if state != last_state:
                if state == 0:
                    message = "ledOn"
                    print(f"Sending command : {message}")
                    await espnow.asend(peer, message)
                else:
                    message = "ledOff"
                    print(f"Sending command : {message}")
                    await espnow.asend(peer, message)
                last_state = state
        await asyncio.sleep_ms(10)  # Adjust the polling interval as needed
        


# Async function for reading and sending potentiometer data
async def send_potentiometer_data(espnow):
    while True:
        potentiometer_value = adc.read()
        message = f"potentiometer:{potentiometer_value}"
        espnow.send(peer, message)
        await asyncio.sleep(1)  # Send every 1 second
        
        
async def main(espnow):
    await asyncio.gather(send_button_state(espnow), send_potentiometer_data(espnow))
        
        
asyncio.run(main(esp))
