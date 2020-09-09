import time
from adafruit_motorkit import MotorKit

class Car():
    def __init__(self):
        self.gear_lv = 1 # Initialized gear level
        self.gear_unit = 0.1 # gear level changing unit
        self.act_time = 0.2
        self.act_pct = 0.6
        self.kit = MotorKit()
        
    def run(self, m1=0, m2=0, m3=0, m4=0):
        self.kit.motor1.throttle = -m1 * self.gear_lv
        self.kit.motor2.throttle = -m2 * self.gear_lv
        self.kit.motor3.throttle = m4 * self.gear_lv
        self.kit.motor4.throttle = m3 * self.gear_lv
        
    def stop(self):
        self.kit.motor1.throttle = 0
        self.kit.motor2.throttle = 0
        self.kit.motor3.throttle = 0
        self.kit.motor4.throttle = 0

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
            
    def drive(self, steer=0, gear=0):
        m_left = self._steer_val(val=steer)
        m_right = self._steer_val(val=-steer)
        self.run(m_left*gear, m_right*gear, m_left*gear, m_right*gear)

    def _steer_val(self, val, oy=1, ny=-1):
        if oy == ny:
            return oy
        else:
            px = (1-oy)/(oy-ny)
            if val <-1 or val >1:
                print("steer_val error")
                return None
            elif val < px and val > -1:
                return oy+val*(oy-ny)
            elif val == -1:
                return -1
            else:
                return 1
