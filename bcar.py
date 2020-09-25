from bcar.car import Car
from bcar.panel import NineButton
import ipywidgets.widgets as widgets
from ipywidgets import HBox, VBox
import time

class BasicCar():
    def __init__(self):
        self.car = Car()
        self.panel = NineButton()
        self.controller = None
        self.m_steer = 0
        self.m_gear = 0
        self.press_count = 0
    
    def _setting(self):
        self.panel.buttons[0].on_click(lambda x: self.car.forward(p=0.3, t=-1))
        self.panel.buttons[1].on_click(lambda x: self.car.forward())
        self.panel.buttons[2].on_click(lambda x: self.car.slide_left(p=0.5, t=-1)) #
        self.panel.buttons[3].on_click(lambda x: self.car.left())
        self.panel.buttons[4].on_click(lambda x: self.car.stop())
        self.panel.buttons[5].on_click(lambda x: self.car.right())
        self.panel.buttons[6].on_click(lambda x: self.car.backward(p=0.3, t=-1))
        self.panel.buttons[7].on_click(lambda x: self.car.backward())
        self.panel.buttons[8].on_click(lambda x: self.car.slide_right(p=0.5, t=-1)) #
        
    def play(self):
        self._setting()
        return self.panel.display()

    def _car_axes_rl(self, change):
        self.m_steer = change['new']
        self.car.drive(steer=self.m_steer, gear=self.m_gear)

    def _car_axes_fb(self, change):
        self.m_gear = - change['new']
        self.car.drive(steer=self.m_steer, gear=self.m_gear)
        
    def _slide_left(self, change):
        val = change['new']
        if self.controller.buttons[5].value == 0:
            if val == 1:
                self.car.run(m1=0.6, m2=-0.6, m3=-0.6, m4=0.6)
            if val == 0:
                self.car.run(m1=0, m2=0, m3=0, m4=0)
    
    def _slide_right(self, change):
        val = change['new']
        if self.controller.buttons[4].value == 0:
            if val == 1:
                self.car.run(m1=-0.6, m2=0.6, m3=0.6, m4=-0.6)
            if val == 0:
                self.car.run(m1=0, m2=0, m3=0, m4=0)
            
    def joystick_setup(self, index=0, display=False):
        self.controller = widgets.Controller(index=index)
        display(self.controller) if display==True else print("Now, move your Joystick a bit to activiate...")
        
    def joystick_on(self): # Linking js to car movement control
        self.controller.axes[0].observe(self._car_axes_rl, names=['value'])
        self.controller.axes[3].observe(self._car_axes_fb, names=['value'])
        
        self.controller.buttons[12].observe(lambda x: self._press_act(event="forward")) # forward
        self.controller.buttons[13].observe(lambda x: self._press_act(event="backward")) # backward
        self.controller.buttons[14].observe(lambda x: self._press_act(event="left")) # turn left
        self.controller.buttons[15].observe(lambda x: self._press_act(event="right")) # turn right
        
        self.controller.buttons[4].observe(self._slide_left, names=['value']) # Sliding car to left
        self.controller.buttons[5].observe(self._slide_right, names=['value']) # Sliding car to right

    def joystick_off(self): # Unlinking js to car movement control
        self.controller.axes[0].unobserve(self._car_axes_rl, names=['value'])
        self.controller.axes[3].unobserve(self._car_axes_fb, names=['value'])
        
    def _press_act(self, event):
        self.press_count += 1
        if self.press_count > 7:
            if event == "forward":
                self.car.forward()
            elif event == "backward":
                self.car.backward()
            elif event == "left":
                self.car.left()
            elif event == "right":
                self.car.right()
            self.press_count = 0
        
class OmniCar():
    def __init__(self):
        pass