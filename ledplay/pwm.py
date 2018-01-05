import RPi.GPIO as GPIO
import time
from random import choice, randint

ALL = 18, 23, 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALL, GPIO.OUT)

pwms = [GPIO.PWM(c, 500) for c in ALL]
for pwm in pwms:
    pwm.start(100)

for n in range(100):
    choice(pwms).ChangeDutyCycle(randint(0, 100))
    time.sleep(.3)
    
GPIO.cleanup()
