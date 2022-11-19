from machine import Pin, Timer

ON_BOARD_PIN = 2
led_pin = Pin(ON_BOARD_PIN, Pin.OUT)

def toggle_led(t):
    led_pin.value(not led_pin.value())

led_timer = Timer(1)
led_timer.init(mode=Timer.PERIODIC,period=1000,callback=toggle_led)