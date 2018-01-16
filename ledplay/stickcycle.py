from gpiozero import PWMLED
import colorsys
from time import sleep
import sys
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 11
MISO =  9
MOSI = 10
CS   =  8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

ALL = 14, 20, 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(ALL, GPIO.OUT)

pwms = [GPIO.PWM(c, 500) for c in ALL]
for pwm in pwms:
    pwm.start(0)

try:
    while True:
        hue = mcp.read_adc(0)
        brightness = mcp.read_adc(1)
        rgb = colorsys.hsv_to_rgb(hue / 1023, 1, brightness / 1023)
        for i, value in enumerate(rgb):
            pwms[i].ChangeDutyCycle(value * 100)
            sleep(.05)
except:
    pass

GPIO.cleanup()

