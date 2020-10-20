import time
import bcar.motordriver as md
from bcar.adjuster import adjust_axes, adjust_steer

class Car():
    def __init__(self, model=0):
        self.gear_lv = 0.5 # Initialized gear level
        self.gear_unit = 0.1 # gear level changing unit
        self.act_time = 0.2
        self.act_pct = 0.3
        if model == 0:
            self.motor = md.PCA9685()
        elif model == 1:
            self.motor = md.PCA9685_Plus_GPIO()
        elif model == 2:
            self.motor = md.AdafruitFeatherwing()
        
    def run(self, m1=0, m2=0, m3=0, m4=0):
        self.motor.m1_act(val=-m1*self.gear_lv)
        self.motor.m2_act(val=m2*self.gear_lv)
        self.motor.m3_act(val=-m3*self.gear_lv)
        self.motor.m4_act(val=m4*self.gear_lv)
        
    def stop(self):
        self.run(m1=0, m2=0, m3=0, m4=0)

    def forward(self, p=None, t=None):
        p=self.act_pct if p==None else p
        t=self.act_time if t==None else t
        self.run(p,p,p,p)
        if t== -1:
            pass
        else:
            time.sleep(t)
            self.stop()

    def backward(self, p=None, t=None):
        p=self.act_pct if p==None else p
        t=self.act_time if t==None else t
        self.run(-p,-p,-p,-p)
        if t== -1:
            pass
        else:
            time.sleep(t)
            self.stop()

    def right(self, p=None, t=None):
        p=self.act_pct if p==None else p
        t=self.act_time if t==None else t
        self.run(p,-p,p,-p)
        if t== -1:
            pass
        else:
            time.sleep(t)
            self.stop()

    def left(self, p=None, t=None):
        p=self.act_pct if p==None else p
        t=self.act_time if t==None else t
        self.run(-p,p,-p,p)
        if t== -1:
            pass
        else:
            time.sleep(t)
            self.stop()
            
    def slide_left(self, p=None, t=None):
        p=self.act_pct if p==None else p
        t=self.act_time if t==None else t
        self.run(p,-p,-p,p)
        if t== -1:
            pass
        else:
            time.sleep(t)
            self.stop()

    def slide_right(self, p=None, t=None):
        p=self.act_pct if p==None else p
        t=self.act_time if t==None else t
        self.run(-p,p,p,-p)
        if t== -1:
            pass
        else:
            time.sleep(t)
            self.stop()
            
    def level_up(self):
        if self.gear_lv + self.gear_unit < 1:
            self.gear_lv = round(self.gear_lv + self.gear_unit, 1)
        else:
            self.gear_lv = 1
        print(self.gear_lv)

    def level_down(self):
        if self.gear_lv - self.gear_unit > 0.4:
            self.gear_lv = round(self.gear_lv - self.gear_unit, 1)
        else:
            self.gear_lv = 0.4
        print(self.gear_lv)
    
    def level_read(self):
        print(self.gear_lv)
            
    def drive(self, steer=0, gear=0):
        m_left, m_right = adjust_steer(val=adjust_axes(val=steer, adj_x=0.9, adj_y=0.6), center_y=0.8, peak_y=-0.7)
        self.run(m_left*gear*self.gear_lv, m_right*gear*self.gear_lv, m_left*gear*self.gear_lv, m_right*gear*self.gear_lv)