from time import time, sleep

from leds import light_winner, light_non_winner
from settings import *
from logger import logger


def handle_player_responses(players, queue, correct_sequence, valid_press_start):
    timeout = time() + MAX_REACTION_TIME_PER_SEQUENCE_ELEMENT * len(correct_sequence)
    finished_players = []

    while time() < timeout and len(finished_players) < len(players):
        for player in players:
            if player not in finished_players:
                presses = player.presses
                pressed_buttons = [press.index for press in presses]
                if presses:
                    logger.info('%s: %s. Correct: %s' % (player.name, pressed_buttons, correct_sequence))
                if pressed_buttons == correct_sequence and presses[0].time > valid_press_start:
                    elapsed = presses[-1].time - valid_press_start
                    player.record_completion(elapsed)
                    if len(finished_players) == 0:  # This is the winner
                        queue.put('%s wins in %d milliseconds' % (player.name, int(elapsed * 1000)))
                        player.wins += 1
                        light_winner(player)
                    elif GAME_MODE == GameMode.Sequence:
                        light_non_winner(player)
                    finished_players.append(player)
        sleep(.1)

    return finished_players
