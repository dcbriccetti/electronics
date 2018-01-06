import RPi.GPIO as GPIO
from time import sleep
import colorsys
from random import choice, randint

ALL = 18, 24, 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALL, GPIO.OUT)

pwms = [GPIO.PWM(c, 500) for c in ALL]
for pwm in pwms:
    pwm.start(0)

for hue in range(1000):
    rgb = colorsys.hsv_to_rgb(hue / 1000, 1, 1)
    for i, value in enumerate(rgb):
        pwms[i].ChangeDutyCycle(value * 100)
        sleep(.01)
    
GPIO.cleanup()
