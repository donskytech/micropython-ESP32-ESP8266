import network
import aioespnow
import machine
import asyncio

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# Initialize ESP-NOW
esp = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
esp.active(True)

led_pin = machine.Pin(22, machine.Pin.OUT)

async def wait_for_message():
    while True:
        _, msg = esp.recv()
        if msg:             # msg == None if timeout in recv()
            if msg == b'ledOn':
                print("Turning on LED")
                led_pin.on()
            elif msg == b'ledOff':
                print("Turning off LED")
                led_pin.off()
            else:
                print("Unknown message!")
            

asyncio.run(wait_for_message())
