from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont
from collections.deque import deque
import utime

class TFTDisplay:
    MAX_AVAIL_TFT_DISPLAY_LINES = 5
    
    def __init__(self):
        self.spi = SPI(2, baudrate=40000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
        self.display = Display(self.spi, dc=Pin(33), cs=Pin(5), rst=Pin(32), rotation=0)
        self.font_small = XglcdFont('fonts/Bally7x9.c', 7, 9)
        self.font_large = XglcdFont('fonts/ArcadePix9x11.c', 9, 11)
        self.queue = deque()
        
    def cleanup(self):
        print('Cleaning up display...')
        self.display.cleanup()
        
    # Schedule is a tuple of (soil_moisture_name, date)
    def add_water_cycle(self, schedule):
        if len(self.queue) >= TFTDisplay.MAX_AVAIL_TFT_DISPLAY_LINES:
            self.queue.popright()
        self.queue.appendleft(schedule)
        self.update_water_cycle_list()
        
    def update_water_cycle_list(self):
        self.display.fill_rectangle(20, 0, 220, 150, color565(0, 0, 0))
        position = 0
        for index, value in enumerate(self.queue):
            print(f"Index: {index}, Value: {value}")
            soil_moisture_name, water_date = value
            position += 20
            self.display.draw_text(position , 150, soil_moisture_name, self.font_small,
                      color565(0, 0, 255),
                      landscape=True)
            position += 20
            self.display.draw_text(position, 150, water_date, self.font_small,
                      color565(0, 255, 0),
                      landscape=True)
            
        
    def update_sensor_readings(self, position, value):
        if position == 0:
            self.display.fill_rectangle(40, 180, 20, 140, color565(0, 0, 0))
            self.display.draw_text(40, 320, value, self.font_small,
                      color565(0, 255, 0),
                      landscape=True)
        elif position == 1:
            self.display.fill_rectangle(80, 180, 20, 140, color565(0, 0, 0))
            self.display.draw_text(80, 320, value, self.font_small,
                      color565(0, 255, 0),
                      landscape=True)
        elif position == 2:
            self.display.fill_rectangle(120, 180, 20, 140, color565(0, 0, 0))
            self.display.draw_text(120, 320, value, self.font_small,
                      color565(0, 255, 0),
                      landscape=True)
    
    def display_init_ui(self):
        self.display.clear(color565(255, 255, 255))
        self.display.clear()
        #  Draw Sensor Readings       
        self.display.draw_text(0, 300, 'SENSOR READINGS', self.font_large,
                      color565(0, 255, 0),
                      landscape=True)
        
        self.display.draw_text(20, 320, 'Sensor Module 1', self.font_small,
                      color565(0, 0, 255),
                      landscape=True)
        
        self.display.draw_text(40, 320, 'N/A', self.font_large,
                      color565(0, 255, 0),
                      landscape=True)
        
        self.display.draw_text(60, 320, 'Sensor Module 2', self.font_small,
                      color565(0, 0, 255),
                      landscape=True)
        
        self.display.draw_text(80, 320, 'N/A', self.font_large,
                      color565(0, 255, 0),
                      landscape=True)
        
        self.display.draw_text(100, 320, 'Sensor Module 3', self.font_small,
                      color565(0, 0, 255),
                      landscape=True)
        
        self.display.draw_text(120, 320, 'N/A', self.font_large,
                      color565(0, 255, 0),
                      landscape=True)
        
        self.display.draw_hline(20, 160, 200, color565(255, 255, 255))
        
        #  Draw Water Cycle
        self.display.draw_text(0, 120, 'Water Cycle', self.font_large,
                      color565(0, 255, 0),
                      landscape=True)
        
        
        
    
    
# tft_display = TFTDisplay()
# tft_display.display_init_ui()
# sleep(2)
# print('Updating Sensor Readings..')
# tft_display.update_sensor_readings(0, "35000")
# sleep(2)
# tft_display.update_sensor_readings(1, "45000")
# sleep(2)
# tft_display.update_sensor_readings(2, "55000")
# sleep(2)
# tft_display.update_sensor_readings(0, "42000")
# sleep(2)
# tft_display.update_sensor_readings(0, "38000")
# sleep(2)
# tft_display.update_sensor_readings(1, "23000")
# sleep(2)
# tft_display.update_sensor_readings(2, "25000")
# sleep(2)
# 
# 
# print('Adding water cycle')
# tft_display.add_water_cycle(('Soil Moisture 1', '2023-11-15 14:20'))
# print('---------')
# sleep(1)
# tft_display.add_water_cycle(('Soil Moisture 2', '2023-11-15 14:30'))
# print('---------')
# sleep(1)
# tft_display.add_water_cycle(('Soil Moisture 3', '2023-11-15 14:40'))
# print('---------')
# sleep(1)
# tft_display.add_water_cycle(('Soil Moisture 1', '2023-11-15 14:50'))
# print('---------')
# sleep(1)
# tft_display.add_water_cycle(('Soil Moisture 3', '2023-11-15 14:52'))
# print('---------')
# sleep(1)
# tft_display.add_water_cycle(('Soil Moisture 2', '2023-11-15 14:55'))
# print('---------')
# sleep(1)
# 
# tft_display.cleanup()

    
    

