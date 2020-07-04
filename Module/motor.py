import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) 

# Pin 18 19 ; IN 1 2 => 左前輪
# Pin 21 22 ; IN 3 4 => 左後輪
# Pin 23 24 ; IN 5 6 => 右前輪
# Pin 11 13 ; IN 7 8 => 右後輪

class Direction():
    def __init__(self, dc = 50.0):
        #-----------------------motor
        GPIO.setup(18,GPIO.OUT)
        GPIO.setup(19,GPIO.OUT)
        GPIO.setup(21,GPIO.OUT)
        GPIO.setup(22,GPIO.OUT)
        GPIO.setup(23,GPIO.OUT)  
        GPIO.setup(24,GPIO.OUT)  
        GPIO.setup(38,GPIO.OUT)  
        GPIO.setup(40,GPIO.OUT)

        GPIO.output(18,GPIO.LOW)
        GPIO.output(19,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
        GPIO.output(22,GPIO.LOW)
        GPIO.output(23,GPIO.LOW)  
        GPIO.output(24,GPIO.LOW)
        GPIO.output(38,GPIO.LOW)  
        GPIO.output(40,GPIO.LOW)

        #-----------------------pwm
        GPIO.setup(12,GPIO.OUT)
        GPIO.setup(32,GPIO.OUT)
        GPIO.setup(33,GPIO.OUT)
        GPIO.setup(35,GPIO.OUT)
        
        self.pwm0 = GPIO.PWM(12, 50.0)
        self.pwm1 = GPIO.PWM(32, 50.0)
        self.pwm2 = GPIO.PWM(33, 50.0)
        self.pwm3 = GPIO.PWM(35, 50.0)
        
        self.dc = dc
        self.pwm0.start(self.dc)
        self.pwm1.start(self.dc)
        self.pwm2.start(self.dc + 5)
        self.pwm3.start(self.dc + 5)
    
    # car directions
    def Dir(self, direction):
        if direction == 'F':
            GPIO.output(19,GPIO.HIGH)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(23,GPIO.HIGH)
            GPIO.output(24,GPIO.LOW)     
            GPIO.output(40,GPIO.HIGH)
            GPIO.output(38,GPIO.LOW)
        if direction == 'R':
            GPIO.output(19,GPIO.LOW)
            GPIO.output(18,GPIO.HIGH)
            GPIO.output(22,GPIO.LOW)
            GPIO.output(21,GPIO.HIGH)
            GPIO.output(23,GPIO.HIGH)  
            GPIO.output(24,GPIO.LOW)  
            GPIO.output(40,GPIO.HIGH)  
            GPIO.output(38,GPIO.LOW) 
        if direction == 'L':
            GPIO.output(19,GPIO.HIGH)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(22,GPIO.HIGH)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(23,GPIO.LOW)  
            GPIO.output(24,GPIO.HIGH)  
            GPIO.output(40,GPIO.LOW)  
            GPIO.output(38,GPIO.HIGH) 
        if direction == 'B':
            GPIO.output(19,GPIO.LOW)
            GPIO.output(18,GPIO.HIGH)   
            GPIO.output(22,GPIO.LOW)
            GPIO.output(21,GPIO.HIGH)
            GPIO.output(23,GPIO.LOW)
            GPIO.output(24,GPIO.HIGH)
            GPIO.output(40,GPIO.LOW)
            GPIO.output(38,GPIO.HIGH)
        if direction == 'S':
            GPIO.output(19,GPIO.LOW)
            GPIO.output(18,GPIO.LOW)
            GPIO.output(22,GPIO.LOW)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(23,GPIO.LOW)  
            GPIO.output(24,GPIO.LOW)  
            GPIO.output(40,GPIO.LOW)  
            GPIO.output(38,GPIO.LOW)
    
    # change duty cycle
    def Update_dc(self, dif):
        if (dif < -1.0):
            self.dc = self.dc * dif * -1.0
            if (self.dc > 100.0):
                self.dc = 100.0
            self.pwm2.ChangeDutyCycle(self.dc)
            self.pwm3.ChangeDutyCycle(self.dc)
            
        elif (dif > 1.0):
            self.dc = self.dc / dif
            self.pwm2.ChangeDutyCycle(self.dc)
            self.pwm3.ChangeDutyCycle(self.dc)
            
        return self.dc