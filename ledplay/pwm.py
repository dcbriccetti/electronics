import RPi.GPIO as GPIO
import time
from random import choice, randint

ALL = 18, 23, 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALL, GPIO.OUT)

pwms = [GPIO.PWM(c, 500) for c in ALL]
for pwm in pwms:
    pwm.start(0)

r = range(0, 101, 10)
for redDc in r:
    pwms[0].ChangeDutyCycle(redDc)
    for greenDc in r:
        print(redDc, greenDc)
        pwms[1].ChangeDutyCycle(greenDc)
        for blueDc in r:
            pwms[2].ChangeDutyCycle(blueDc)
            time.sleep(.01)
    
GPIO.cleanup()
