from espnow_node import EspNowNode
from wifi_node import WiFiNode
import asyncio
import wifi_config
import network
import aioespnow
from machine import I2C, Pin
import ujson
from lcd_i2c import LCD
from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
import time
from primitives import Queue

queue = Queue()


MAC_0 = '78:21:84:C6:38:B0'
b_MAC = [bytes([int(i, 16) for i in mac.split(':')]) for mac in [MAC_0]]

# wifi = WiFiNode()
espnow = EspNowNode(peers_mac=b_MAC)


# MicroDot
# Initialize MicroDot
app = Microdot()
Response.default_content_type = 'text/html'

# root route
@app.route('/')
async def index(request):
    return render_template('index.html')


@app.route('/ws')
@with_websocket
async def read_queue(request, ws):
    while True:
        message = await queue.get()
        if message is not None:
            print("ESP-NOW message is received")
            string_message = message.decode('utf-8')
            await ws.send(string_message)

# Static CSS/JSS
@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


# shutdown
@app.get('/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'    
    
async def server():
    print("Ready to serve Web Request")
    await app.start_server(port=80)
        
async def wait_for_message():
    async for mac, msg in espnow.node:
        if msg:
            try:
                print(f"Message :: {msg}")
                await queue.put(msg)
                msg = ujson.loads(msg)    
            except ValueError as e:
                print(f"Parsing Error: {e}")
            else:                
                print(msg)
#                 if "pir_alert_detected" in msg:
#                     await trigger_pir_alert(msg)
#                 elif "infrared_alert_detected" in msg:
#                     await trigger_infrared_alert(msg)
#                 elif "temperature"  in msg:
#                     await display_temp_humidity(msg)
                    
                


async def main():
#     await asyncio.gather(wait_for_message(), server())
#     asyncio.create_task(server())
# #     asyncio.create_task(runForever())
#     while True:
#         await asyncio.sleep_ms(1)	# time after that the device stops running
    print('Starting main program')
    await asyncio.gather(wait_for_message(), server())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Interrupted')
finally:
    asyncio.new_event_loop()
