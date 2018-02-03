from time import time, sleep

from ledcolors import GREEN, OFF
from settings import MAX_REACTION, MIN_REACTION, WIN_BLINK_TIME, WIN_BLINKS


def handle_player_responses(players, queue, react_color_indexes):
    start = time()
    timeout = start + MAX_REACTION
    complete = []

    while time() < timeout and len(complete) < len(players):
        for player in players:
            if player not in complete:
                pp = player.presses
                pressed_indexes = [press.index for press in pp]
                if pressed_indexes == react_color_indexes and pp[0].time > start + MIN_REACTION:
                    player.led.off()
                    elapsed = time() - start
                    player.record_completion(elapsed)
                    if len(complete) == 0:  # This is the winner
                        winner_msg = '%s wins in %d milliseconds' % (player.name, int(elapsed * 1000))
                        queue.put(winner_msg)
                        player.wins += 1
                        player.led.blink(WIN_BLINK_TIME, WIN_BLINK_TIME, 0, 0, GREEN, OFF, WIN_BLINKS)
                    complete.append(player)
        sleep(.001)
    return complete