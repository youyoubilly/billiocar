from bcar.car import Car
import ipywidgets.widgets as widgets
from ipywidgets import HBox, VBox, Button
import time

class BCar():
    def __init__(self):
        self.car = Car()
        self.panel = ButtonGroup()
        self.m_steer = 0
        self.m_gear = 0
        self.press_count = 0
        
    def play(self):
        self._setting()
        return self.panel.display()

    def _car_axes_rl(self, change):
        self.m_steer = change['new']
        self.car.drive(steer=self.m_steer, gear=self.m_gear)

    def _car_axes_fb(self, change):
        self.m_gear = - change['new']
        if abs(self.m_gear) > 0.1:
            self.car.drive(steer=self.m_steer, gear=self.m_gear)
        else:
            self.car.drive(steer=0, gear=0)
        
    def _slide_left(self, change):
        val = change['new']
        pct = 0.6
        if self.controller.buttons[5].value == 0:
            if val == 1:
                self.car.run(m1=pct, m2=-pct, m3=-pct, m4=pct)
            if val == 0:
                self.car.run(m1=0, m2=0, m3=0, m4=0)
    
    def _slide_right(self, change):
        val = change['new']
        pct = 0.6
        if self.controller.buttons[4].value == 0:
            if val == 1:
                self.car.run(m1=-pct, m2=pct, m3=pct, m4=-pct)
            if val == 0:
                self.car.run(m1=0, m2=0, m3=0, m4=0)
            
    def controller_setup(self, index=0):
        self.controller = widgets.Controller(index=index)
        print("Move your controller NOW and activiate it...")
        display(self.controller)
        
    def controller_on(self): # Linking js to car movement control
        self.controller.axes[0].observe(self._car_axes_rl, names=['value'])
        self.controller.axes[3].observe(self._car_axes_fb, names=['value'])
        
        self.controller.buttons[12].observe(lambda x: self._press_act(event="forward")) # forward
        self.controller.buttons[13].observe(lambda x: self._press_act(event="backward")) # backward
        self.controller.buttons[14].observe(lambda x: self._press_act(event="left")) # turn left
        self.controller.buttons[15].observe(lambda x: self._press_act(event="right")) # turn right
        
        self.controller.buttons[4].observe(lambda x: self._press_act(event="level_down")) # gear level up
        self.controller.buttons[5].observe(lambda x: self._press_act(event="level_up")) # gear level up
        
        self.controller.buttons[10].observe(self._slide_left, names=['value']) # Sliding car to left
        self.controller.buttons[11].observe(self._slide_right, names=['value']) # Sliding car to right
        
    def _setting(self): #config for actions
        self.panel.buttons[0].on_click(lambda x: self.car.forward(p=0.3, t=-1))
        self.panel.buttons[1].on_click(lambda x: self.car.forward())
        self.panel.buttons[2].on_click(lambda x: self.car.slide_left(p=0.5, t=-1))
        self.panel.buttons[3].on_click(lambda x: self.car.left())
        self.panel.buttons[4].on_click(lambda x: self.car.stop())
        self.panel.buttons[5].on_click(lambda x: self.car.right())
        self.panel.buttons[6].on_click(lambda x: self.car.backward(p=0.3, t=-1))
        self.panel.buttons[7].on_click(lambda x: self.car.backward())
        self.panel.buttons[8].on_click(lambda x: self.car.slide_right(p=0.5, t=-1))
        
        self.panel.extra[0].on_click(lambda x: self.car.level_up())
        self.panel.extra[1].on_click(lambda x: self.car.level_read())
        self.panel.extra[2].on_click(lambda x: self.car.level_down())
        
    def _press_act(self, event):
        self.press_count += 1
        if self.press_count > 8:
            if event == "forward":
                self.car.forward()
            elif event == "backward":
                self.car.backward()
            elif event == "left":
                self.car.left()
            elif event == "right":
                self.car.right()
            elif event == "level_up":
                self.car.level_up()
            elif event == "level_read":
                self.car.level_read()
            elif event == "level_down":
                self.car.level_down()
            self.press_count = 0
            
class ButtonGroup():
    def __init__(self, button_list=None):
        self.button_layout = widgets.Layout(width='60px', height='40px', align_self='center')
        self.button_list = ['Fwd', '▲', 'sL', '◄', 'Stop', '►', 'Bwd', '▼', 'sR'] if button_list==None else button_list
        self.extra_list = ['UP_lv', '-', 'DOWN_lv']
        self.buttons = [Button(description=i, layout=self.button_layout) for i in self.button_list]
        self.extra = [Button(description=i, layout=self.button_layout) for i in self.extra_list]
        
    def display(self):
        row1 = HBox([self.buttons[0], self.buttons[1], self.buttons[2]])
        row2 = HBox([self.buttons[3], self.buttons[4], self.buttons[5]])
        row3 = HBox([self.buttons[6], self.buttons[7], self.buttons[8]])
        col1 = VBox([self.extra[0], self.extra[1], self.extra[2]])
        return HBox([VBox([row1, row2, row3]), col1])