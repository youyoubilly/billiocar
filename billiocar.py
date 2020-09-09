from car import Car
from panel import NineButton

class Basic():
    def __init__(self):
        self.car = Car()
        self.panel = NineButton()
    
    def _setting(self):
        self.panel.buttons[0].on_click(lambda x: self.car.forward(p=0.3, t=-1))
        self.panel.buttons[1].on_click(lambda x: self.car.forward())
        self.panel.buttons[3].on_click(lambda x: self.car.left())
        self.panel.buttons[4].on_click(lambda x: self.car.stop())
        self.panel.buttons[5].on_click(lambda x: self.car.right())
        self.panel.buttons[6].on_click(lambda x: self.car.backward(p=0.3, t=-1))
        self.panel.buttons[7].on_click(lambda x: self.car.backward())
        
    def play(self):
        self._setting()
        return self.panel.display()