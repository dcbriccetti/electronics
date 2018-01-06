from gpiozero import LED, MotionSensor
from time import sleep

leds = red, green, blue = [LED(pin) for pin in (18, 23, 24)]
green.on()
pir = MotionSensor(25)

try:
    while True:
        pir.wait_for_motion()
        green.off()
        while pir.motion_detected:
            for n in range(10):
                red .blink(.1, 0, 1, background=False)
                blue.blink(.1, 0, 1, background=False)
        green.on()
except KeyboardInterrupt:
    pass

for led in leds:
    led.off()
