'LEDs controller'

from time import sleep
from ledcolors import GREEN, OFF
from settings import BUTTON_COLORS


def flash_leds(color_indexes, players):
    'Flash once for each color index (into BUTTON_COLORS), for each player.'

    for i in color_indexes:
        for player in players:
            player.led.color = BUTTON_COLORS[i]
        sleep(.2)
        for player in players:
            player.led.off()
        sleep(.2)


def light_winner(player):
    'Signal the winner'
    player.led.blink(0.1, 0.1, 0, 0, GREEN, OFF, 3)


def light_non_winner(player):
    'Signal a player who completed the sequence, but who wasn’t first'
    player.led.blink(0.2, 0, 0, 0, GREEN, OFF, 1)
