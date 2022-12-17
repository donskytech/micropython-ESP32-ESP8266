from machine import Pin, SoftI2C
import ssd1306
import framebuf
import time

# using default address 0x3C
i2c = SoftI2C(sda=Pin(22), scl=Pin(23))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.fill(0)                         # fill entire screen with colour=0
# display.pixel(0, 10)                    # get pixel at x=0, y=10
# display.pixel(0, 10, 1)                 # set pixel at x=0, y=10 to colour=1
# display.hline(0, 32, 128, 1)               # draw horizontal line x=0, y=8, width=4, colour=1
# display.vline(0, 8, 4, 1)               # draw vertical line x=0, y=8, height=4, colour=1
# display.line(0, 0, 127, 63, 1)          # draw a line from 0,0 to 127,63
display.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1
# display.fill_rect(10, 10, 107, 43, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1
# display.text('Hello World', 0, 0, 1)    # draw some text at x=0, y=0, colour=1
# display.scroll(120, 0)                   # scroll 20 pixels to the right

# display.fill_rect(14,11,20,40,1)
# display.fill_rect(36,11,20,40,1)
# display.fill_rect(58,11,20,40,1)
# display.fill_rect(80,11,20,40,1)
x_pos = [12, 38, 64, 90]
percentages = [.25, .50, .75, 1.0]
while True:
    
    for ctr in range(4):
        display.fill_rect(x_pos[ctr],11,24,40,1)
        display.fill_rect(0,56,128,40,0)
        display.text("{:.0%}".format(percentages[ctr]), 11, 56)
        display.show()
        time.sleep_ms(1000)
        
    for ctr in range(4):
        display.fill_rect(x_pos[ctr],11,24,40,0)
        
    display.show()
        





