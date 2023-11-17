from machine import Pin
import ds1302

# ds = ds1302.DS1302(Pin(25),Pin(26),Pin(27))
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
        
    def get_unformatted_date_time(self):
        return self.rtc.date_time()
        
    def get_current_date_time(self):
        rtc_datetime = self.rtc.date_time()
        year, month, day, day_of_the_week, hour, minute, second = self.rtc.date_time()
        print(year, month, day, day_of_the_week, hour, minute, second)
        formatted_datetime = f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
#         print("Formatted Date and Time:", formatted_datetime)
        return formatted_datetime
    