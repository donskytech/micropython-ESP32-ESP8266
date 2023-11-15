from soil_monitor_module import SoilMonitor, NotEnoughDataError
import config
import ujson
from system_rtc_clock import RTCClock

class AutoFarmSystem:
    def __init__(self, rtc_clock, message_queue):
        soil_monitor_pos_1 = SoilMonitor(config.SOIL_MONITOR_ID_1, config.SOIL_MONITOR_MODULE_1)
        soil_monitor_pos_2 = SoilMonitor(config.SOIL_MONITOR_ID_2, config.SOIL_MONITOR_MODULE_2)
        soil_monitor_pos_3 = SoilMonitor(config.SOIL_MONITOR_ID_3, config.SOIL_MONITOR_MODULE_3)
        
        self.soil_monitors = {config.SOIL_MONITOR_ID_1: soil_monitor_pos_1, config.SOIL_MONITOR_ID_2: soil_monitor_pos_2,
                              config.SOIL_MONITOR_ID_3: soil_monitor_pos_3}
        
        self.watering_cycle = []
        self.rtc_clock = rtc_clock
        self.message_queue = message_queue
        
    def clear_cycle_list(self):
        print("Clearing water cycle list")
        self.watering_cycle.clear()
        
    def get_cycle_list(self):
        print("Clearing water cycle list")
        return self.watering_cycle
        
        
    async def process_message(self, message):
        try:
            json_message = ujson.loads(message)  
        except ValueError as e:
            print(f"Parsing Error: {e}")
            return
        else:
            json_message['event_type'] = 'updateSensorReadings'
            print(json_message)
            await self.message_queue.put(json_message)
        
        
        current_soil_monitor = self.soil_monitors.get(json_message[config.SOIL_MONITOR_KEY], None)
        
        if current_soil_monitor:
            
            try:
                current_soil_monitor.enqueue(json_message['sensor_reading'])
                current_average_reading = current_soil_monitor.get_average_reading()
                print(f"current_average_reading: {current_average_reading}")
#                 
#                 print(f"Valve Status : {current_soil_monitor.valve_status}")
                if current_soil_monitor.get_valve_status():
                    if current_average_reading <= config.WET_SOIL_READING:
                        current_soil_monitor.close_valve()
                else:
                    if current_average_reading >= config.DRY_SOIL_READING:
                        self.watering_cycle.append({"date_time": self.rtc_clock.get_current_date_time(), "soil_module": current_soil_monitor.get_name()})
                        print(self.watering_cycle)
                        watering_cycle_event = {'event_type': 'updateWaterCycle', "date_time": self.rtc_clock.get_current_date_time(), "soil_module": current_soil_monitor.get_name()}
                        await self.message_queue.put(watering_cycle_event)
                        current_soil_monitor.open_valve()
                    
                
            except NotEnoughDataError:
                print("Not enough data...")
                pass
        else:
            print("Wala")

        
# auto_farm_system = AutoFarmSystem()
# auto_farm_system.process_message("{\"soil_monitor\": \"Soil Monitor 1\", \"sensor_reading\":  65535} ")
# 
# auto_farm_system.process_message("{\"soil_monitor\": \"Soil Monitor 1\", \"sensor_reading\":  62000} ")
# 
# auto_farm_system.process_message("{\"soil_monitor\": \"Soil Monitor 1\", \"sensor_reading\":  61000} ")
# 
# auto_farm_system.process_message("{\"soil_monitor\": \"Soil Monitor 1\", \"sensor_reading\":  60000} ")
# 
# auto_farm_system.process_message("{\"soil_monitor\": \"Soil Monitor 1\", \"sensor_reading\":  55000} ")
# 
# auto_farm_system.process_message("{\"soil_monitor\": \"Soil Monitor 1\", \"sensor_reading\":  52000} ")
