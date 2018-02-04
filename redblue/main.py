# Reaction Time Game

from queue import Empty
from flask import Flask, render_template
from flask_json import FlaskJSON, as_json
from gameloop import GameLoop
from player import Player

game = GameLoop((Player('One',   buttons=(16, 12), led=(26, 19, 13)),
                 Player('Two',   buttons=(21, 20), led=( 2,  3,  4)),
#                Player('Three', buttons=(23, 24), led=(17, 27, 22))))  Not working yet
                 ))
app = Flask(__name__)
json = FlaskJSON(app)


def names_and_scores():
    sorted_players = list(game.players)
    sorted_players.sort(key=lambda player: player.wins, reverse=True)
    names_scores = [
        [p.name, p.wins, p.fastest_ms() or '', p.mean_ms() or '', p.slowest_ms() or '']
        for i, p in enumerate(sorted_players)]
    return names_scores


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/reset")
@as_json
def reset():
    for player in game.players:
        player.reset()
    return {}


@app.route("/status")
@as_json
def status():
    try:
        event = game.queue.get(timeout=5)  # Without timeout, old threads will consume events after a browser reload
    except Empty:
        event = None
    return {'event': event, 'scores': names_and_scores()} if event else None


@app.route("/statusNoWait")
@as_json
def status_nowait():
    names_scores = names_and_scores()
    return {'scores': names_scores}

app.run(host='localhost', threaded=True)
