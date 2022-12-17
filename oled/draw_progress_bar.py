from machine import Pin, SoftI2C
import ssd1306
import framebuf
import time

# using default address 0x3C
i2c = SoftI2C(sda=Pin(22), scl=Pin(23))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.fill(0)                         # fill entire screen with colour=0
display.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to width=107, height=53, colour=1

# draw battery percentage
x_pos = [12, 38, 64, 90]
percentages = [.25, .50, .75, 1.0]
while True:
    for ctr in range(4):
        display.fill_rect(x_pos[ctr],11,24,40,1)
        display.fill_rect(0,56,128,40,0)
        display.text("{:.0%}".format(percentages[ctr]), 11, 56)
        display.show()
        time.sleep_ms(1000)
    
    # This will clear the battery charge percentage
    for ctr in range(4):
        display.fill_rect(x_pos[ctr],11,24,40,0)
        
    display.show()
        





