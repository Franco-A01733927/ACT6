import serial
import Adafruit_SSD1306
import Adafruit_GPIO.SPI as SPI

import time 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import gpiozero  # The GPIO library for Raspberry Pi
led = gpiozero.LED(17) # Reference GPIO17

# Raspberry Pi pin configuration:
RST = 24

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

font = ImageFont.load_default()
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

def main():
    disp.begin()
    draw.rectangle((0,0,128,64),outline=0,fill=0) #Clear the display
    f = open("prueba.txt","w")
    f.write('0')
    f.close()
    n = 0
    line = "0"
    while 1:
        draw.text((31,18),  "ACTUAL SCORE:",  font=font, fill=255)
        #take sarial data from Arduino
        f=open('prueba.txt','r')
        line = f.read()
        f.close()
        if (str(n) == line):
            n+=1
        draw.text((63,31), str(line),  font=font, fill=255)
        # Display image.
        disp.image(image)
        disp.display()
        draw.rectangle((0,0,128,64),outline=0,fill=0) #Clear the display
        f2=open('prueba2.txt','r')
        lt = f2.read()
        ledtime = float(lt)
        led.on() # Turn the LED on
        time.sleep(ledtime)
        led.off() # Turn the LED off
        time.sleep(ledtime)  # Pause for 1 second
        f2.close()


if __name__ == '__main__':
    main()
