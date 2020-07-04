# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from flask import Flask

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(40,GPIO.IN)

#-----------------------
#Trig => 38
#Echo => 40

def Ultrasonic():
    GPIO.output(38,GPIO.HIGH)
    time.sleep(0.0015)
    GPIO.output(38,GPIO.LOW)
    
    t1 = time.time()
    
    while not GPIO.input(40):
        pass
    
    t2 = time.time()
    
    return (t2-t1)*340/2