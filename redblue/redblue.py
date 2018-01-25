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
MIN_WAIT = 1.5
MAX_WAIT = 5
MAX_REACTION = 2.5
MIN_REACTION = .060
WAIT_RANGE = MAX_WAIT - MIN_WAIT
WIN_BLINK_TIME = .3
WIN_BLINKS = 1

players = (Player('One', (16, 12), (26, 19, 13)),
           Player('Two', (21, 20), (2, 3, 4)))
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
    for player in players:
        player.reset()
    return {}


@app.route("/status")
@as_json
def status():
    event = queue.get()
    names_scores = _names_and_scores()
    return {'event': event, 'scores': names_scores}


@app.route("/statusNoWait")
@as_json
def status_nowait():
    names_scores = _names_and_scores()
    return {'scores': names_scores}


def _names_and_scores():
    sorted_players = players_by_score()
    names_scores = [
        [p.name, p.wins, p.fastest_ms() or '', p.mean_ms() or '', p.slowest_ms() or '']
        for i, p in enumerate(sorted_players)]
    return names_scores


def find_winners(react_color_idx):
    start = time()
    timeout = start + MAX_REACTION
    complete = []

    while time() < timeout and len(complete) < len(players):
        for player in players:
            if player not in complete:
                pp = player.presses
                if len(pp) == 1 and pp[0].index == react_color_idx and pp[0].time > start + MIN_REACTION:
                    player.led.off()
                    elapsed = time() - start
                    player.record_completion(elapsed)
                    if len(complete) == 0:  # This is the winner
                        queue.put('\n%s wins in %d milliseconds' % (player.name, int(elapsed * 1000)))
                        player.wins += 1
                        player.led.blink(WIN_BLINK_TIME, WIN_BLINK_TIME, 0, 0, (0, 1, 0), (0, 0, 0), WIN_BLINKS)
                    complete.append(player)
        sleep(.001)
    return complete


def game_thread():
    while True:
        react_color_idx = randint(0, 1)
        sleep(MIN_WAIT + random() * WAIT_RANGE)
        for player in players:
            player.clear_old_clicks()
            player.led.color = react_colors[react_color_idx]
        complete = find_winners(react_color_idx)
        for player in players:
            if not complete or player is not complete[0]:
                player.led.off()


threading.Thread(target=game_thread).start()
app.run(host='localhost', threaded=True)
