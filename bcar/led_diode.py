import Adafruit_PCA9685
import ipywidgets.widgets as widgets
from ipywidgets import HBox, VBox, Button

class Led_Diode():
    def __init__(self, vcc=15, gnd=14, bus=1):
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=bus)
        self.pwm.set_pwm_freq(50)
        self.pwm.set_pwm(gnd, 0, 0)
        self.vcc = vcc
        self.pct = 0
        self.HIGH = 4095
        self.unit = 0.2
        self.panel = ButtonGroup()
        self.tmp = 0
        self.press_count = 0

    def on(self, pct=1):
        self.tmp = 1
        if pct>1:
            self.pct = 1
        elif pct<0:
            self.pct = 0
        else:
            self.pct = round(pct,1)
        self.pwm.set_pwm(self.vcc, 0, round(self.HIGH*self.pct))
            
    def off(self):
        self.tmp = 0
        self.pct = 0
        self.on(pct=self.pct)
        
    def on_off(self):
        if self.tmp == 0:
            self.on()
            self.tmp = 1
        else:
            self.off()
            self.tmp = 0
        
    def light_up(self, t=1):
        if self.pct + t * self.unit > 1:
            self.pct = 1
        else:
            self.pct = self.pct + t * self.unit
        self.on(pct=self.pct)
    
    def light_down(self, t=1):
        if self.pct - t * self.unit < 0:
            self.pct = 0
        else:
            self.pct = self.pct - t * self.unit
        self.on(pct=self.pct)
        
    def play(self):
        self._setting()
        return self.panel.display()
        
    def _setting(self): #config for actions
        self.panel.buttons[0].on_click(lambda x: self.on_off())
        self.panel.buttons[1].on_click(lambda x: self.light_up())
        self.panel.buttons[2].on_click(lambda x: self.light_down())
        
    def controller_setup(self, index=0):
        self.controller = widgets.Controller(index=index)
        print("Move your controller NOW and activiate it...")
        display(self.controller)
                
    def controller_on(self): # Linking js to led control
        self.controller.buttons[8].observe(lambda x: self._press_act(event="on_off"))
        
    def _press_act(self, event):
        self.press_count += 1
        if self.press_count > 7:
            if event == "on_off":
                self.on_off()
            self.press_count = 0
        
class ButtonGroup():
    def __init__(self, button_list=None):
        self.button_layout = widgets.Layout(width='60px', height='40px')
        self.button_list = ['TL', '☀', '☼'] if button_list==None else button_list
        self.buttons = [Button(description=i, layout=self.button_layout) for i in self.button_list]
        
    def display(self):
        col = VBox([self.buttons[0], self.buttons[1], self.buttons[2]])
        return col