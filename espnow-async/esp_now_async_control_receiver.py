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
pwm_pin = machine.Pin(23, machine.Pin.OUT)
pwm = machine.PWM(machine.Pin(pwm_pin), freq=1000, duty=0)

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

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
            elif msg.startswith(b'potentiometer'):
                string_data = msg.decode('utf-8')
                potentiometer_value = string_data.split(":")[1]
                print(f"Pot Value: {potentiometer_value}")
                # Map the potentiometer value to PWM duty cycle (0 to 1023)
                duty_cycle = int(map_value(int(potentiometer_value), 0, 4095, 0, 1023))
                pwm.duty(duty_cycle)
            else:
                print(f"Unknown message {msg}")
            

asyncio.run(wait_for_message())

