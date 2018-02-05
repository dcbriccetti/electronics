from time import time, sleep

from leds import signal_winner, signal_non_winner
from settings import *


def handle_player_responses(players, queue, correct_sequence, valid_press_start):
    timeout = time() + MAX_REACTION_TIME_PER_SEQUENCE_ELEMENT * len(correct_sequence)
    finished_players = []

    def round_active(): return time() < timeout and len(finished_players) < len(players)

    def unfinished_players(): return (p for p in players if p not in finished_players)

    while round_active():
        for player in unfinished_players():
            def good_button_input():
                pressed_buttons = [press.index for press in player.presses]
                return pressed_buttons == correct_sequence and not player.presses[0].time < valid_press_start

            if good_button_input():
                elapsed = player.presses[-1].time - valid_press_start
                player.record_completion(elapsed)
                if len(finished_players) == 0:  # This is the winner
                    queue.put('%s wins in %d milliseconds' % (player.name, int(elapsed * 1000)))
                    player.wins += 1
                    signal_winner(player)
                elif GAME_MODE == GameMode.Sequence:
                    signal_non_winner(player)  # In sequence mode everybody who finishes in time gets a signal
                finished_players.append(player)

        sleep(.1)

    return finished_players
