class PCA9685():  
    def __init__(self, bus=1):
        import Adafruit_PCA9685
        #Initialize PCA9685 board
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=bus)
        self.pwm.set_pwm_freq(50)
        #Signal and EnA by PWM, setting for each motor
        #Wiring for the BcarBoard
        self.m1_sig, self.m1_in2, self.m1_in1 = 0, 2, 1
        self.m2_sig, self.m2_in2, self.m2_in1 = 11, 9, 10
        self.m3_sig, self.m3_in2, self.m3_in1 = 5, 3, 4
        self.m4_sig, self.m4_in2, self.m4_in1 = 6, 8, 7
        #Wiring for DIY
#         self.m1_sig, self.m1_in1, self.m1_in2 = 0, 4, 5
#         self.m2_sig, self.m2_in1, self.m2_in2 = 1, 6, 7
#         self.m3_sig, self.m3_in1, self.m3_in2 = 2, 8, 9
#         self.m4_sig, self.m4_in1, self.m4_in2 = 3, 10, 11
        self.HIGH = 4095

    def motor_act(self, sig, in1, in2, val=0):
        if val > 0:
            self.pwm.set_pwm(in1, 0, self.HIGH)
            self.pwm.set_pwm(in2, 0, 0)
        elif val < 0:
            self.pwm.set_pwm(in1, 0, 0)
            self.pwm.set_pwm(in2, 0, self.HIGH)
        else:
            self.pwm.set_pwm(in1, 0, 0)
            self.pwm.set_pwm(in2, 0, 0)
        self.pwm.set_pwm(sig, 0, abs(val))
        
    def m1_act(self, val=0):
        self.motor_act(self.m1_sig, self.m1_in1, self.m1_in2, round(self.HIGH*val))

    def m2_act(self, val=0):
        self.motor_act(self.m2_sig, self.m2_in1, self.m2_in2, round(self.HIGH*val))
        
    def m3_act(self, val=0):
        self.motor_act(self.m3_sig, self.m3_in1, self.m3_in2, round(self.HIGH*val))
        
    def m4_act(self, val=0):
        self.motor_act(self.m4_sig, self.m4_in1, self.m4_in2, round(self.HIGH*val))

    def stop(self):
        self.m1_act(val=0)
        self.m2_act(val=0)
        self.m3_act(val=0)
        self.m4_act(val=0)  

class PCA9685_Plus_GPIO():  
    def __init__(self, bus=1):
        #Initialize PCA9685 board
        import Adafruit_PCA9685
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=bus)
        self.pwm.set_pwm_freq(50)
        #Signal by PWM, EnA by GPIO, setting for each motor
        self.m1_sig, self.m1_in1, self.m1_in2 = 0, 31, 33
        self.m2_sig, self.m2_in1, self.m2_in2 = 1, 35, 37
        self.m3_sig, self.m3_in1, self.m3_in2 = 2, 32, 36
        self.m4_sig, self.m4_in1, self.m4_in2 = 3, 38, 40
        # set pin numbers to the board's
        import Jetson.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        #Initialize EnA, In1 and In2
        GPIO.setup(self.m1_in1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.m1_in2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.m2_in1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.m2_in2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.m3_in1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.m3_in2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.m4_in1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.m4_in2, GPIO.OUT, initial=GPIO.LOW)
        self.HIGH = 4095

    def motor_act(self, sig, in1, in2, val=0):
        if val > 0:
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
        elif val < 0:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
        else:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.LOW)
        self.pwm.set_pwm(sig, 0, abs(val))
        
    def m1_act(self, val=0):
        self.motor_act(self.m1_sig, self.m1_in1, self.m1_in2, round(self.HIGH*val))

    def m2_act(self, val=0):
        self.motor_act(self.m2_sig, self.m2_in1, self.m2_in2, round(self.HIGH*val))
        
    def m3_act(self, val=0):
        self.motor_act(self.m3_sig, self.m3_in1, self.m3_in2, round(self.HIGH*val))
        
    def m4_act(self, val=0):
        self.motor_act(self.m4_sig, self.m4_in1, self.m4_in2, round(self.HIGH*val))
        
    def stop(self):
        self.m1_act(val=0)
        self.m2_act(val=0)
        self.m3_act(val=0)
        self.m4_act(val=0)        
        
    def shutdown():
        self.stop()
        GPIO.cleanup()
        
class AdafruitFeatherwing():  
    def __init__(self):
        from adafruit_motorkit import MotorKit
        self.kit = MotorKit()
        
    def m1_act(self, val=0):
        self.kit.motor1.throttle = -val

    def m2_act(self, val=0):
        self.kit.motor2.throttle = -val
        
    def m3_act(self, val=0):
        self.kit.motor3.throttle = val
        
    def m4_act(self, val=0):
        self.kit.motor4.throttle = val