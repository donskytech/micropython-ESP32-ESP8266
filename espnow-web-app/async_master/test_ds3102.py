from machine import Pin
import ds1302

ds = ds1302.DS1302(Pin(5),Pin(18),Pin(19))

print(ds.date_time()) # returns the current datetime.
# ds.date_time([2023, 11, 13, 0, 8, 51, 0]) # set datetime.
# 
# ds.hour() # returns hour.
# ds.second(10) # set second to 10.
# print(ds.date_time())