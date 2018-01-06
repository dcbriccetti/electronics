import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
RGB = RED, GREEN, BLUE = 18, 23, 24
PIR_IN = 25
GPIO.setup(RGB, GPIO.OUT)
GPIO.setup(PIR_IN, GPIO.IN)

try:
    while True:
        if (GPIO.input(PIR_IN)):
            GPIO.output(GREEN, 0)
            for n in range(10):
                GPIO.output(RED, 1)
                sleep(.1)
                GPIO.output(RED, 0)
                GPIO.output(BLUE, 1)
                sleep(.1)
                GPIO.output(BLUE, 0)
            sleep(1.5)
            GPIO.output(GREEN, 1)
        sleep(.1)
except KeyboardInterrupt:
    pass

print('done')
for pin in RGB:
    GPIO.output(pin, 0)
    
GPIO.cleanup()
