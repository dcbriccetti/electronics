from time import time
from gpiozero import RGBLED, Button
from buttonpress import ButtonPress
from settings import DISCARD_PRESSES_OLDER_THAN


def to_ms(value):
    return int(value * 1000)


class Player:
    'Information about a player, including buttons, the LED, and game performance'

    def __init__(self, name, buttons, led):
        self.name = name
        self.buttons = [self._create_button(index, pin) for index, pin in enumerate(buttons)]
        self.led = RGBLED(*led, pwm=False)
        self.wins = 0
        self.presses = []
        self.elapsed_times = []

    def clear_old_clicks(self):
        time_now = time()
        self.presses = [press for press in self.presses
                        if time_now - press.time < DISCARD_PRESSES_OLDER_THAN]

    def record_completion(self, elapsed_time):
        self.elapsed_times.append(elapsed_time)

    def reset(self):
        self.wins = 0
        self.elapsed_times = []

    def fastest_ms(self):
        return to_ms(min(self.elapsed_times)) if self.elapsed_times else None

    def mean_ms(self):
        return to_ms(sum(self.elapsed_times) / len(self.elapsed_times)) if self.elapsed_times else None

    def slowest_ms(self):
        return to_ms(max(self.elapsed_times)) if self.elapsed_times else None

    def _pressed(self, index):
        self.presses.append(ButtonPress(index, time()))

    def _create_button(self, index, pin):
        button = Button(pin)
        button.when_pressed = lambda: self._pressed(index)
        return button
