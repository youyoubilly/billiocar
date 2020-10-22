import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=0, gpio=1)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 10
# Load default font.
font = ImageFont.load_default()
# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font1 = ImageFont.truetype('editundo.ttf', 16)
# font2 = ImageFont.truetype('small_pixel-7.ttf', 14)

import subprocess

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )

    # Write two lines of text.
    localdate = time.strftime("%m-%d %a", time.localtime()) 
    localtime = time.strftime("%H:%M:%S", time.localtime()) 
    draw.text((x, top),"Hi! BillioCar", font=font1, fill=255)
#     draw.text((x+27, top+13),localdate, font=font2, fill=255)
    draw.text((x+8, top+11),str(IP)[2:-3],  font=font2, fill=255)
    draw.text((x+30, top+20),localtime, font=font2, fill=255)


    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)