from time import sleep
from random import random, randint
import threading
from queue import Queue, Empty

from ledcolors import BLUE, RED
from responses import handle_player_responses
from settings import *


class GameLoop:
    def __init__(self, players):
        self.players = players
        self.react_colors = RED, BLUE
        self.queue = Queue()

        threading.Thread(target=self._game_thread, name='GameLoop').start()

    def players_by_score(self):
        sorted_players = list(self.players)
        sorted_players.sort(key=lambda player: player.wins, reverse=True)
        return sorted_players

    def names_and_scores(self):
        sorted_players = self.players_by_score()
        names_scores = [
            [p.name, p.wins, p.fastest_ms() or '', p.mean_ms() or '', p.slowest_ms() or '']
            for i, p in enumerate(sorted_players)]
        return names_scores

    def reset_players(self):
        for player in self.players:
            player.reset()

    def get_event(self):
        try:
            event = self.queue.get(timeout=5)  # Without timeout, old threads will consume events after a browser reload
        except Empty:
            event = None
        return event

    def _game_thread(self):
        while True:
            react_color_indexes = [randint(0, len(self.react_colors) - 1)
                                   for n in range(1 + randint(0, MAX_SEQUENCE_LENGTH - 1))]
            sleep(MIN_WAIT + random() * WAIT_RANGE)

            for player in self.players:
                player.clear_old_clicks()

            for react_color_index in react_color_indexes:
                for player in self.players:
                    player.led.color = self.react_colors[react_color_index]
                sleep(.3)
                for player in self.players:
                    player.led.off()
                sleep(.1)

            handle_player_responses(self.players, self.queue, react_color_indexes)
