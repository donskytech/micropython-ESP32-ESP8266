from machine import Pin
import utime

# Define the GPIO pin where the relay is connected
relay_pin = Pin(23, Pin.OUT)  # Change the pin number as per your setup

# Function to turn on the relay
def turn_relay_on():
    relay_pin.on()
    print("Relay turned ON")

# Function to turn off the relay
def turn_relay_off():
    relay_pin.off()
    print("Relay turned OFF")

# Main loop
while True:
    turn_relay_on()
    utime.sleep(2)  # Wait for 2 seconds
    turn_relay_off()
    utime.sleep(2)  # Wait for 2 seconds
