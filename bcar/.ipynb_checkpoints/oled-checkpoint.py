import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

class OLED():
    def __init__(self, bus=1):
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=bus, gpio=1)
        self.disp.begin()
        self.disp.clear()
        self.disp.display()
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.padding = -2
        self.top = self.padding
        self.bottom = self.height-self.padding
        self.x = 10
        self.font = ImageFont.load_default()
        
    def clear(self):
        self.disp.clear()
        self.disp.display()
        
    def ip(self):
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True)
        self.draw.text((self.x+8, self.top+11),str(IP)[2:-3], font=self.font, fill=255)
        self.disp.image(self.image)
        self.disp.display()

    def pic(self, path):
        self.clear()
        self.image = Image.open(path).convert('1')
        self.disp.image(self.image)
        self.disp.display()

#     def default(self, path):
#         self.clear()
#         self.image = Image.open(path).convert('1')
#         cmd = "hostname -I | cut -d\' \' -f1"
#         IP = subprocess.check_output(cmd, shell = True)
#         self.draw.text((self.x+8, self.top+18),str(IP)[2:-3], font=self.font, fill=255)
#         self.disp.image(self.image)
#         self.disp.display()
