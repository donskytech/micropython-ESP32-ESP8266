'''
    Description:  LED Light show using MicroPython with ESP32 and ESP8266 board
    Author:		  donskytech
'''

from machine import Pin, Timer
from utime import sleep_ms

led_pin_numbers = [23, 22, 21, 19, 18, 5, 17, 16]
led_pins = []

OFF = 0
ON = 1

SHORT_SLEEP_MS = 100
MEDIUM_SLEEP_MS = 500

# Setup
def setup_pins():
    for pin in led_pin_numbers:
        led_pins.append(Pin(pin, Pin.OUT))

def turn_off_leds():
    for pin in led_pins:
        pin.value(OFF)
        
def turn_on_leds():
    for pin in led_pins:
        pin.value(ON)

def running_leds():
    for _ in range(2):
        for pin in led_pins:
            turn_off_leds()
            pin.value(ON)
            sleep_ms(SHORT_SLEEP_MS)
        
        for pin in reversed(led_pins):
            turn_off_leds()
            pin.value(ON)
            sleep_ms(SHORT_SLEEP_MS)
        
def mixer_leds():
    turn_off_leds()
    for pin in led_pins:
        pin.value(ON)
        sleep_ms(SHORT_SLEEP_MS)
        
    turn_off_leds()
    for pin in reversed(led_pins):
        pin.value(ON)
        sleep_ms(SHORT_SLEEP_MS)
        
def blink_blink_leds():    
    for _ in range(5):
        turn_on_leds()
        sleep_ms(SHORT_SLEEP_MS)
        turn_off_leds()
        sleep_ms(SHORT_SLEEP_MS)    
        
def odd_even_leds():
    turn_off_leds()
    for pin in led_pins[::2]:
        pin.value(ON)
        sleep_ms(MEDIUM_SLEEP_MS)
        
    turn_off_leds()
    for pin in led_pins[1::2]:
        pin.value(ON)
        sleep_ms(MEDIUM_SLEEP_MS)
    
    turn_off_leds()
    for pin in led_pins[-1::-2]:
        pin.value(ON)
        sleep_ms(MEDIUM_SLEEP_MS)
        
    turn_off_leds()
    for pin in led_pins[-2::-2]:
        pin.value(ON)
        sleep_ms(MEDIUM_SLEEP_MS)
        
def dual_blink_leds():
    for _ in range(2):
        for index in [2,6,0,4]:
            turn_off_leds()
            for pin in led_pins[index:index+2:]:
                pin.value(ON)
            sleep_ms(MEDIUM_SLEEP_MS)
            
def led_light_show(t):
    led_effects = [blink_blink_leds, running_leds, dual_blink_leds, mixer_leds, odd_even_leds]
    
    for effect in led_effects:
        effect()
        
#     blink_blink_leds()
#     running_leds()
#     dual_blink_leds()
#     mixer_leds()
#     odd_even_leds()
    

def main():
    setup_pins()

    led_timer = Timer(1)
    led_timer.init(mode=Timer.PERIODIC,period=1000,callback=led_light_show)

if __name__ == '__main__':
    main()
