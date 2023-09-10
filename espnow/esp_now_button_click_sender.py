import network
from machine import Pin
import espnow
import utime


# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Define the MAC address of the receiving ESP32 (ESP32 B)
peer = b'x!\x84\xc68\xb0'
esp.add_peer(peer)

# Create a function to send data when a button is pressed (optional)
button_pin = Pin(23, Pin.IN, Pin.PULL_UP)

# Initialize variables for debouncing
last_button_state = 1  # Assuming the button is not pressed initially
debounce_delay = 50  # Adjust this value to your needs (milliseconds)

while True:
    # Read the current state of the button
    current_button_state = button_pin.value()
    
    # Check if the button state has changed
    if current_button_state != last_button_state:
        # Wait for a short time to debounce the button
        utime.sleep_ms(debounce_delay)
        
        # Read the button state again to make sure it's stable
        current_button_state = button_pin.value()
        
        # If the button state is still different, it's a valid press
        if current_button_state != last_button_state:
            if current_button_state == 0:
                message = "ledOn"
                print(f"Sending command : {message}")
                esp.send(peer, message)
            else:
                message = "ledOff"
                print(f"Sending command : {message}")
                esp.send(peer, message)
        
        # Update the last button state
        last_button_state = current_button_state
        