import network
import aioespnow
import asyncio
from machine import Pin

# A WLAN interface must be active to send()/recv()
network.WLAN(network.STA_IF).active(True)

esp = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
esp.active(True)
peer = b'x!\x84\xc68\xb0'
esp.add_peer(peer)

# Create a function to send data when a button is pressed (optional)
button_pin = Pin(23, Pin.IN, Pin.PULL_UP)
debounce_delay = 50  # Adjust this value to your needs (milliseconds)


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
        
        
asyncio.run(send_button_state(esp))