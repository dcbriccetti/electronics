from time import time, sleep
from random import random, randint
import threading
from queue import Queue
from player import Player

# Times below are in seconds
MIN_WAIT = 1.5
MAX_WAIT = 5
MAX_REACTION = 2.5
MIN_REACTION = .060
WAIT_RANGE = MAX_WAIT - MIN_WAIT
WIN_BLINK_TIME = .3
WIN_BLINKS = 1


class GameLoop:
    def __init__(self):
        self.players = (Player('One', (16, 12), (26, 19, 13)),
                        Player('Two', (21, 20), (2, 3, 4)))
        self.react_colors = (1, 0, 0), (0, 0, 1)
        self.queue = Queue()

        threading.Thread(target=self._game_thread).start()

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
        return self.queue.get()

    def _game_thread(self):
        def find_winners():
            start = time()
            timeout = start + MAX_REACTION
            complete = []

            while time() < timeout and len(complete) < len(self.players):
                for player in self.players:
                    if player not in complete:
                        pp = player.presses
                        if len(pp) == 1 and pp[0].index == react_color_idx and pp[0].time > start + MIN_REACTION:
                            player.led.off()
                            elapsed = time() - start
                            player.record_completion(elapsed)
                            if len(complete) == 0:  # This is the winner
                                self.queue.put('\n%s wins in %d milliseconds' % (player.name, int(elapsed * 1000)))
                                player.wins += 1
                                player.led.blink(WIN_BLINK_TIME, WIN_BLINK_TIME, 0, 0, (0, 1, 0), (0, 0, 0), WIN_BLINKS)
                            complete.append(player)
                sleep(.001)
            return complete

        while True:
            react_color_idx = randint(0, 1)
            sleep(MIN_WAIT + random() * WAIT_RANGE)
            for player in self.players:
                player.clear_old_clicks()
                player.led.color = self.react_colors[react_color_idx]
            complete = find_winners()
            for player in self.players:
                if not complete or player is not complete[0]:
                    player.led.off()
