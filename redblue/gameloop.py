import threading
from queue import Queue
from random import random, randint
from time import sleep, time

from leds import flash_leds
from responses import handle_player_responses
from settings import *


class GameLoop:
    def __init__(self, players):
        self.players = players
        self.queue = Queue()

        threading.Thread(target=self._game_thread, name='GameLoop').start()

    def _game_thread(self):
        def random_color():
            return randint(0, len(BUTTON_COLORS) - 1)

        def random_color_sequence():
            return [random_color() for n in range(randint(SEQUENCE_RANGE[0], SEQUENCE_RANGE[1]))]

        while True:
            sleep(MIN_WAIT + (0 if GAME_MODE == GameMode.Sequence else random() * WAIT_RANGE))
            valid_press_start = time()
            color_indexes = random_color_sequence() if GAME_MODE == GameMode.Sequence else [1]
            flash_leds(color_indexes, self.players)

            for player in self.players:
                player.clear_all_clicks() if GAME_MODE == GameMode.Sequence else player.clear_old_clicks()

            handle_player_responses(self.players, self.queue, color_indexes, valid_press_start)
