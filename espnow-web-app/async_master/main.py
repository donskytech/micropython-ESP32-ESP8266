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
from auto_farm_system import AutoFarmSystem
from system_rtc_clock import RTCClock

rtc_clock = RTCClock()
message_queue = Queue()
auto_farm_system = AutoFarmSystem(rtc_clock, message_queue)

MAC_0 = '78:21:84:C6:38:B0'
b_MAC = [bytes([int(i, 16) for i in mac.split(':')]) for mac in [MAC_0]]

wifi = WiFiNode()
espnow = EspNowNode(peers_mac=b_MAC)


# Initialize MicroDot
app = Microdot()
Response.default_content_type = 'text/html'

# root route
@app.route('/')
async def index(request):
    cycle_list = auto_farm_system.get_cycle_list()
    return render_template('index.html', cycle_list=cycle_list)


@app.route('/ws')
@with_websocket
async def read_queue(request, ws):
    while True:
        message = await message_queue.get()
        print(f"Message from queue : {message}")
        if message is not None:
            await ws.send(ujson.dumps(message))

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
    print("Starting Web Server")
    await app.start_server(port=80)
        
async def wait_for_message():
    print("Getting ready to receive ESP-NOW Messages")
    async for mac, msg in espnow.node:
        if msg:
#             print(f"Message Received :: {msg}, putting to queue")
#             await message_queue.put(msg)
            
            string_message = msg.decode('utf-8')
            await auto_farm_system.process_message(string_message)
            
async def clear_cycle_list():
    while True:
        print("Checking if it is time to clear the cycle list..")
        current_datetime = rtc_clock.get_unformatted_date_time()
        print(f"current_datetime : {current_datetime}")
        hour = current_datetime[4]
        minute = current_datetime[5]
        if hour == 0 and minute == 0:
            print("Clearing cycle list..")
            auto_farm_system.clear_cycle_list()
        await asyncio.sleep_ms(60000) 
    

    
    
#             try:
#                 print(f"Message Received :: {msg}, putting to queue")
#                 
# #                 msg = ujson.loads(msg)    
#             except ValueError as e:
#                 print(f"Parsing Error: {e}")
#             else:                
#                 print(msg)
#                 await queue.put(msg)
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
#     await asyncio.gather(wait_for_message())
    await asyncio.gather(wait_for_message(), server(), clear_cycle_list())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Interrupted')
finally:
    asyncio.new_event_loop()
