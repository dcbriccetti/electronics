# Reaction Time Game

from flask import Flask, render_template
from flask_json import FlaskJSON, as_json
from gameloop import GameLoop
from player import Player

game = GameLoop((Player('One',   buttons=(16, 12), led=(26, 19, 13)),
                 Player('Two',   buttons=(21, 20), led=( 2,  3,  4)),
                 Player('Three', buttons=(23, 24), led=(17, 27, 22))))
app = Flask(__name__)
json = FlaskJSON(app)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/reset")
@as_json
def reset():
    game.reset_players()
    return {}


@app.route("/status")
@as_json
def status():
    event = game.get_event()
    return {'event': event, 'scores': game.names_and_scores()} if event else None


@app.route("/statusNoWait")
@as_json
def status_nowait():
    names_scores = game.names_and_scores()
    return {'scores': names_scores}


app.run(host='localhost', threaded=True)
