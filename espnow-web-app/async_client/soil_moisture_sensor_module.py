import machine
import utime

# adc = machine.ADC(32)

# while True:
#     moisture = adc.read_u16() 
#     print(moisture)
#     utime.sleep_ms(1000)
    
class SoilMonitor:
    def __init__(self):
        self.adc = machine.ADC(32)
    
    def read_soil_moisture(self):
        moisture = self.adc.read_u16()
        return moisture
