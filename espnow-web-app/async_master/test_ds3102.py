from machine import Pin
import ds1302

# ds = ds1302.DS1302(Pin(5),Pin(18),Pin(19))
# 
# print(ds.date_time()) # returns the current datetime.
# ds.date_time([2023, 11, 13, 0, 8, 51, 0]) # set datetime.
# 
# ds.hour() # returns hour.
# ds.second(10) # set second to 10.
# print(ds.date_time())

class RTCClock:
    def __init__(self):
        self.rtc = ds1302.DS1302(Pin(25),Pin(26),Pin(27))
        
    def get_current_date_time(self):
        return self.rtc.date_time()
    
rtc_clock = RTCClock()
date_time_details = rtc_clock.get_current_date_time()
print(date_time_details)

hour = date_time_details[4]
minute = date_time_details[5]

print(hour)
print(minute)