from time import time
from gpiozero import RGBLED, Button

KEEP_IF_NEWER_THAN_SECONDS = 1

class Player:
    def __init__(self, name, buttons, led):
        self.name = name
        self.buttons = [self._create_button(index, pin) for index, pin in enumerate(buttons)]
        self.led = RGBLED(*led, pwm=False)
        self.wins = 0
        self.presses = []
        self.elapsed_times = []

    def clear_old_clicks(self):
        time_now = time()
        self.presses = [(index, ptime) for index, ptime in self.presses
                            if time_now - ptime < KEEP_IF_NEWER_THAN_SECONDS]

    def record_completion(self, elapsed_time):
        self.elapsed_times.append(elapsed_time)
        
    def reset(self):
        self.wins = 0
        self.num_completions = 0
        self.elapsed_times = []

    def fastest_ms(self):
        return self._to_ms(min(self.elapsed_times)) if self.elapsed_times else None
    
    def mean_ms(self):
        return self._to_ms(sum(self.elapsed_times) / len(self.elapsed_times)) if self.elapsed_times else None

    def slowest_ms(self):
        return self._to_ms(max(self.elapsed_times)) if self.elapsed_times else None
    
    def _to_ms(self, value):
        return int(value * 1000)

    def _pressed(self, index):
        self.presses.append((index, time()))

    def _create_button(self, index, pin):
        b = Button(pin)
        b.when_pressed = lambda : self._pressed(index)
        return b
