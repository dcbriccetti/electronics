# Reaction Time Game
# Inspired by a project in The Arduino Inventor's Guide

from random import random
from time import sleep, time
from gpiozero import Button, LED

class Player:
    def __init__(self, name, button, led):
        self.name = name
        self.button = Button(button)
        self.led = LED(led)
        self.wins = 0

players = (Player('Black', 16, 13),
           Player('Red',   20, 19),
           Player('White', 21, 26),
           Player('Blue',  12,  6))

def find_winners():
    start = time()
    timeout = start + 4
    
    while time() < timeout:
        winners = [player for player in players if player.button.is_pressed]
        if winners:
            return winners, time() - start
    return [], 0  # Timed out

while True:
    sleep(1 + random() * 3)
    for p in players:
        p.led.blink(.1, 0, 1)
        
    winners, elapsed = find_winners()
    sleep(.4)  # Build suspense about who won
    for player in winners:
        player.led.blink(.05, .05, 10)
        print('\n%s wins in %d milliseconds' % (player.name, elapsed * 1000))
        player.wins += 1

    if winners:
        sorted_players = list(players)
        sorted_players.sort(key=lambda player: player.wins, reverse=True)
        print('Wins:', ', '.join(['%s: %d' % (player.name, player.wins)
                                  for i, player in enumerate(sorted_players)]))
