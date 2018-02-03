from time import time, sleep
from ledcolors import GREEN, OFF
from settings import MAX_REACTION_TIME_PER_SEQUENCE_ELEMENT, GameMode, GAME_MODE


def handle_player_responses(players, queue, react_color_indexes, valid_press_start):
    start = time()
    timeout = start + MAX_REACTION_TIME_PER_SEQUENCE_ELEMENT * len(react_color_indexes)
    complete = []

    while time() < timeout and len(complete) < len(players):
        for player in players:
            if player not in complete:
                pp = player.presses
                pressed_buttons = [press.index for press in pp]
                if pressed_buttons == react_color_indexes and pp[0].time > valid_press_start:
                    player.led.off()
                    elapsed = time() - valid_press_start
                    player.record_completion(elapsed)
                    if len(complete) == 0:  # This is the winner
                        winner_msg = '%s wins in %d milliseconds' % (player.name, int(elapsed * 1000))
                        queue.put(winner_msg)
                        player.wins += 1
                        player.led.blink(0.1, 0.1, 0, 0, GREEN, OFF, 3)
                    elif GAME_MODE == GameMode.Sequence:
                        player.led.blink(0.2, 0, 0, 0, GREEN, OFF, 1)
                    complete.append(player)
        sleep(.1)

    return complete
