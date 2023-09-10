import uasyncio as asyncio
from machine import Pin

# Create a button object (change the GPIO pin as needed)
button_pin = Pin(33, Pin.IN, Pin.PULL_UP)

# Create an event to control coroutine execution
execute_event = asyncio.Event()

# Define a function to enable coroutines
def enable_coroutines():
    execute_event.set()  # Set the event to enable coroutine execution

# Define a function to cancel coroutines
def cancel_coroutines():
    execute_event.clear()  # Clear the event to cancel coroutine execution

# Define an async task that listens for button clicks
async def button_listener():
    while True:
        if not button_pin.value():  # Button is pressed
            print("Button clicked, toggling coroutine execution.")
            if execute_event.is_set():
                cancel_coroutines()
            else:
                enable_coroutines()
            await asyncio.sleep_ms(500)  # Debounce
        await asyncio.sleep_ms(100)  # Check button state every 100ms

# Define your other async coroutines
async def coroutine1():
    while True:
        if execute_event.is_set():  # Check if execution is enabled
            # Your coroutine logic here
            print("Coroutine 1 is running.")
        await asyncio.sleep(1)

async def coroutine2():
    while True:
        if execute_event.is_set():  # Check if execution is enabled
            # Your coroutine logic here
            print("Coroutine 2 is running.")
        await asyncio.sleep(2)

# Create an asyncio event loop
loop = asyncio.get_event_loop()

# Start the button listener task
loop.create_task(button_listener())

# Start your other coroutines as tasks
loop.create_task(coroutine1())
loop.create_task(coroutine2())

try:
    # Run the event loop indefinitely
    loop.run_forever()
except KeyboardInterrupt:
    print("Keyboard interrupt, exiting.")
finally:
    loop.close()
