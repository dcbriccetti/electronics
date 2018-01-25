# Reaction Time Game
# Inspired by a project in The Arduino Inventor's Guide
import threading
from queue import Queue
from random import random, randint
from time import sleep
from time import time

from flask import Flask, render_template
from flask_json import FlaskJSON, as_json
from player import Player

# Times below are in seconds
SUSPENSE_TIME = .4
MIN_WAIT = 1.5
MAX_WAIT = 5
MAX_REACTION = 2.5
MIN_REACTION = .060
WAIT_RANGE = MAX_WAIT - MIN_WAIT
WIN_BLINK_TIME = .3
WIN_BLINKS = 1

players = (Player('One',  (16, 12), (26, 19, 13)),
           Player('Two',  (21, 20), ( 2,  3,  4)))
react_colors = (1, 0, 0), (0, 0, 1)

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
        player.fastest_ms = 0;
    return {}

@app.route("/status")
@as_json
def status():
    event = queue.get()
    sorted_players = players_by_score()
    names_scores = [[player.name, player.wins, player.fastest_ms or '']
                    for i, player in enumerate(sorted_players)]
    return {'event': event, 'scores': names_scores}


def pressing_players(react_color_idx):
    return [player for player in players if player.buttons[react_color_idx].is_pressed]

def find_winners(react_color_idx):
    start = time()
    timeout = start + MAX_REACTION

    while time() < timeout:
        winners = [player for player in players
                   if len(player.presses) == 1
                   and player.presses[0][0] == react_color_idx
                   and player.presses[0][1] > start + MIN_REACTION]
        if winners:
            return winners, time() - start
        sleep(.01)
    return [], 0  # Timed out


def game_thread():
    while True:
        react_color_idx = randint(0, 1)
        sleep(MIN_WAIT + random() * WAIT_RANGE)
        for player in players:
            player.clear_old_clicks()
            player.led.color = react_colors[react_color_idx]
        winners, elapsed = find_winners(react_color_idx)
        for player in players:
            player.led.off()
        sleep(SUSPENSE_TIME)  # Build suspense about who won
        for player in winners:
            player.led.blink(WIN_BLINK_TIME, WIN_BLINK_TIME, 0, 0, (0, 1, 0), (0, 0, 0), WIN_BLINKS)
            elapsed_ms = int(elapsed * 1000)
            queue.put('\n%s wins in %d milliseconds' % (player.name, elapsed_ms))
            if not player.fastest_ms or elapsed_ms < player.fastest_ms:
                player.fastest_ms = elapsed_ms
            player.wins += 1

threading.Thread(target=game_thread).start()
app.run(host='localhost', threaded=True)
