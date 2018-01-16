from time import sleep
from colorsys import hsv_to_rgb
from gpiozero import RGBLED
from Adafruit_MCP3008 import MCP3008

adc = MCP3008(clk=11, cs=8, miso=9, mosi=10)
led = RGBLED(14, 20, 21)

JOY_X = 0      # Which pin on the A/D converter
JOY_Y = 1
MAX_ANALOG = 1023
MAX_HUE = 950  # Stop at violet (avoid wrapping around to red)

try:
    while True:
        joy_x = adc.read_adc(JOY_X)
        joy_y = adc.read_adc(JOY_Y)
        hue = min(joy_x, MAX_HUE)
        brightness = MAX_ANALOG - joy_y  # Invert so up is brightest
        hsv = hue / MAX_ANALOG, 1, brightness / MAX_ANALOG  # Hue, saturation, value
        rgb = hsv_to_rgb(*hsv)  # Red, green, blue
        led.color = rgb
        sleep(1/30)
except KeyboardInterrupt:
    pass

led.off()