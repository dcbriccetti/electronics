# Reaction Time Game
# Inspired by a project in The Arduino Inventor's Guide
import threading
from queue import Queue
from random import random
from time import sleep
from time import time

from flask import Flask, render_template
from flask_json import FlaskJSON, as_json
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

app = Flask(__name__)
json = FlaskJSON(app)
queue = Queue()

def players_by_score():
    sorted_players = list(players)
    sorted_players.sort(key=lambda player: player.wins, reverse=True)
    return sorted_players

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/reset")
@as_json
def reset():
    print('reset')
    for player in players:
        player.wins = 0
    return {}

@app.route("/status")
@as_json
def status():
    event = queue.get()
    sorted_players = players_by_score()
    names_scores = [[player.name, player.wins] for i, player in enumerate(sorted_players)]
    return {'event': event, 'scores': names_scores}


def find_winners():
    start = time()
    timeout = start + 4

    while time() < timeout:
        winners = [player for player in players if player.button.is_pressed]
        if winners:
            return winners, time() - start
    return [], 0  # Timed out


def game_thread():
    while True:
        sleep_secs = 2 + random() * 3
        sleep(sleep_secs)
        for p in players:
            p.led.blink(.1, 0, 1)

        winners, elapsed = find_winners()
        sleep(.4)  # Build suspense about who won
        for player in winners:
            player.led.blink(.05, .05, 3)
            queue.put('\n%s wins in %d milliseconds' % (player.name, elapsed * 1000))
            player.wins += 1

threading.Thread(target=game_thread).start()
app.run(host='localhost', threaded=True)
