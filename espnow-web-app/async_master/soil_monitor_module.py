from collections import deque
import config
from machine import Pin


class NotEnoughDataError(Exception):
    pass

class SoilMonitor:
    def __init__(self, sensor_id, name):
        self.queue = deque()
        self.id = sensor_id
        self.name = name
        self.valve_status = False
        self.relay_pin = Pin(23, Pin.OUT)
        self.close_valve()
        
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
        
    def enqueue(self, reading):
        if reading == 0:
            print("Received zero (0) reading, disregarding...")
            return
        if self.size() >= config.MAX_AVERAGE_READING:
            self.queue.popleft()
            
        return self.queue.append(reading)
    
    def get_average_reading(self):
        if self.size() < config.MAX_AVERAGE_READING:
            raise NotEnoughDataError
        else:
            # Get average of the last readings as defined by the config
            sum_of_readings = sum(self.queue)
            average = sum_of_readings/config.MAX_AVERAGE_READING
            return average
        
    def size(self):
        return len(self.queue)
    
    def open_valve(self):
        self.valve_status = True
        print("Opening Valve..")
        self.relay_pin.off()
        
    def close_valve(self):
        self.valve_status = False
        print("Closing Valve..")
        self.relay_pin.on()
    
    def get_valve_status(self):
        return self.valve_status
        

# soil_monitor = SoilMonitor("id 1")
# 
# try:
#     print("Current queue:", list(soil_monitor.queue))
#     soil_monitor.enqueue(1)
#     print("Current queue:", list(soil_monitor.queue))
# #     print(soil_monitor.get_average_reading())
#     soil_monitor.enqueue(2)
#     print("Current queue:", list(soil_monitor.queue))
# #     print(soil_monitor.get_average_reading())
#     soil_monitor.enqueue(3)
#     print("Current queue:", list(soil_monitor.queue))
# #     print(soil_monitor.get_average_reading())
#     soil_monitor.enqueue(4)
#     print("Current queue:", list(soil_monitor.queue))
# #     print(soil_monitor.get_average_reading())
#     soil_monitor.enqueue(5)
#     print("Current queue:", list(soil_monitor.queue))
#     print(soil_monitor.get_average_reading())
#     soil_monitor.enqueue(6)
#     print("Current queue:", list(soil_monitor.queue))
#     print(soil_monitor.get_average_reading())
# except NotEnoughDataError:
#     print("Not enough data")
# else:
#     print("An unknown error has occured")
    
    
    