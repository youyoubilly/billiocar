import spidev
import sys
import time

import ipywidgets.widgets as widgets
from ipywidgets import HBox, VBox, Button

class SPItoWS():
    def __init__(self, ledc):
        self.led_count = ledc
        self.X = '' # X is signal of WS281x
        for i in range(self.led_count):
            self.X = self.X + "100100100100100100100100100100100100100100100100100100100100100100100100"
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 2400000

    def __del__(self):
        self.spi.close()
        
    def _Bytesto3Bytes(self, num, RGB): # num is number of signal, RGB is 8 bits (1 byte) str
        for i in range(8):
            if RGB[i] == '0':
                self.X = self.X[:num * 3 * 8 + i * 3] + '100' + self.X[num * 3 * 8 + i * 3 + 3:]
            elif RGB[i] == '1':
                self.X = self.X[:num * 3 * 8 + i * 3] + '110' + self.X[num * 3 * 8 + i * 3 + 3:]
    
    def _BytesToHex(self, Bytes):
        return ''.join(["0x%02X " % x for x in Bytes]).strip()
    
    def LED_show(self):
            Y = []
            for i in range(self.led_count * 9):
                Y.append(int(self.X[i*8:(i+1)*8],2))
            WS = self._BytesToHex(Y)
            self.spi.xfer3(Y, 2400000,0,8)

    def RGBto3Bytes(self, led_num, R, G, B):
        if (R > 255 or G > 255 or B > 255):
            print("Invalid Value: RGB is over 255\n")
            sys.exit(1)
        if (led_num > self.led_count - 1):
            print("Invalid Value: The number is over the number of LED")
            sys.exit(1)
        RR = format(R, '08b')
        GG = format(G, '08b')
        BB = format(B, '08b')
        self._Bytesto3Bytes(led_num * 3, GG)
        self._Bytesto3Bytes(led_num * 3 + 1, RR)
        self._Bytesto3Bytes(led_num * 3 + 2, BB)

    def LED_OFF_ALL(self):
        self.X = ''
        for i in range(self.led_count):
            self.X = self.X + "100100100100100100100100100100100100100100100100100100100100100100100100"
        self.LED_show()

class WS2812():
    def __init__(self, led_count = 8):
        self.ledc = led_count
        self.sig = SPItoWS(self.ledc)
        
    def all_on(self,r=255, g=255, b=255):
        for i in range(0, self.ledc):
            self.sig.RGBto3Bytes(i, r, g, b)
        self.sig.LED_show()
    
    def all_inr_on(self, f1=(0,0,0), f2=(255, 255, 0)):
        for i in range(0, self.ledc):
            if i%2 == 0:
                self.sig.RGBto3Bytes(i, f1[0], f1[1], f1[2])
            else:
                self.sig.RGBto3Bytes(i, f2[0], f2[1], f2[2])
        self.sig.LED_show()
        
    def all_off(self):
        self.sig.LED_OFF_ALL()
    
    def on(self, led_id, r=255, g=255, b=255):
        self.sig.RGBto3Bytes(led_id, r, g, b)
        self.sig.LED_show()
        
    def off(self, led_id):
        self.sig.RGBto3Bytes(led_id, 0, 0, 0)
        self.sig.LED_show()
        
    def flash(self, led_id, f1=(0,0,0), f2=(255, 255, 0), rep=3, inr=1):
        if rep == -1:
            while True:
                self.on(led_id, f1[0], f1[1], f1[2])
                time.sleep(inr)
                self.on(led_id, f2[0], f2[1], f2[2])
                time.sleep(inr)
        else:
            for t in range(0, rep):
                self.on(led_id, f1[0], f1[1], f1[2])
                time.sleep(inr)
                self.on(led_id, f2[0], f2[1], f2[2])
                time.sleep(inr)
        self.off(led_id)
        
    def all_flash(self, f1=(0,0,0), f2=(255, 255, 0), rep=3, inr=1):
        if rep == -1:
            while True:
                self.all_on(f1[0], f1[1], f1[2])
                time.sleep(inr)
                self.all_on(f2[0], f2[1], f2[2])
                time.sleep(inr)
        else:
            for t in range(0, rep):
                self.all_on(f1[0], f1[1], f1[2])
                time.sleep(inr)
                self.all_on(f2[0], f2[1], f2[2])
                time.sleep(inr)
        self.all_off()
        
    def police(self, rep=3, inr=1):
        if rep == -1:
            while True:
                self.all_inr_on(f1=(0,0,0), f2=(255, 0, 0))
                time.sleep(inr)
                self.all_inr_on(f1=(0,0,255), f2=(0, 0, 0))
                time.sleep(inr)
        else:
            for t in range(0, rep):
                self.all_inr_on(f1=(0,0,0), f2=(255, 0, 0))
                time.sleep(inr)
                self.all_inr_on(f1=(0,0,255), f2=(0, 0, 0))
                time.sleep(inr)
        self.all_off()

class WS2812_Ctrl():
    def __init__(self):
        self.panel = ButtonGroup()
        self.led = WS2812()
        self.tmp1 = 0
        self.tmp2 = 0
        self.press_count = 0
        
    def play(self):
        self._setting()
        return self.panel.display()
        
    def _setting(self): #config for actions
        self.panel.buttons[0].on_click(lambda x: self.on_off())
        self.panel.buttons[1].on_click(lambda x: self.color_on())
        self.panel.buttons[2].on_click(lambda x: self.led.police())
        
    def on_off(self, r=255, g=255, b=255):
        self.tmp2 = 0
        if self.tmp1 == 0:
            self.led.all_on(r, g, b)
            self.tmp1 = 1
        else:
            self.led.all_off()
            self.tmp1 = 0

    def color_on(self, p=255):
        self.tmp1 = 0
        if self.tmp2 == 0:
            self.led.all_on(p, 0, 0)
            self.tmp2 += 1
        elif self.tmp2 == 1:
            self.led.all_on(0, p, 0)
            self.tmp2 += 1
        elif self.tmp2 == 2:
            self.led.all_on(0, 0, p)
            self.tmp2 += 1
        elif self.tmp2 == 3:
            self.led.all_on(0, p, p)
            self.tmp2 += 1
        elif self.tmp2 == 4:
            self.led.all_on(p, 0, p)
            self.tmp2 += 1
        elif self.tmp2 == 5:
            self.led.all_on(p, p, 0)
            self.tmp2 += 1
        elif self.tmp2 == 6:
            self.led.all_on(p, p, p)
            self.tmp2 = 0
            
    def controller_setup(self, index=0):
        self.controller = widgets.Controller(index=index)
        print("Move your controller NOW and activiate it...")
        display(self.controller)
                
    def controller_on(self): # Linking js to led control
        self.controller.buttons[16].observe(lambda x: self._press_act(event="on_off"))
        
    def _press_act(self, event):
        self.press_count += 1
        if self.press_count > 7:
            if event == "on_off":
                self.on_off()
            self.press_count = 0
            
class ButtonGroup():
    def __init__(self, button_list=None):
        self.button_layout = widgets.Layout(width='60px', height='40px')
        self.button_list = ['HL', '◐', '♮'] if button_list==None else button_list
        self.buttons = [Button(description=i, layout=self.button_layout) for i in self.button_list]
        
    def display(self):
        col = VBox([self.buttons[0], self.buttons[1], self.buttons[2]])
        return col
    