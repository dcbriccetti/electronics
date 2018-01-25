from time import time
from gpiozero import RGBLED, Button

KEEP_IF_NEWER_THAN_SECONDS = 1

class Player:
    def __init__(self, name, buttons, led):
        self.name = name
        self.buttons = [self._create_button(index, pin) for index, pin in enumerate(buttons)]
        self.led = RGBLED(*led, pwm=False)
        self.wins = 0
        self.fastest_ms = None
        self.presses = []

    def clear_old_clicks(self):
        time_now = time()
        self.presses = [(index, ptime) for index, ptime in self.presses
                            if time_now - ptime < KEEP_IF_NEWER_THAN_SECONDS]
        
    def _pressed(self, index):
        self.presses.append((index, time()))
        print(self.presses)

    def _create_button(self, index, pin):
        b = Button(pin)
        b.when_pressed = lambda : self._pressed(index)
        return b
