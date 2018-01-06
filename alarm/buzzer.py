from time import sleep
import RPi.GPIO as GPIO 

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        
    def buzz(self, pitch, duration):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(self.pin, True)
            sleep(delay)
            GPIO.output(self.pin, False)
            sleep(delay)

