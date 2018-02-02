# Reaction Time Game
# Inspired by a project in The Arduino Inventor's Guide
from flask import Flask, render_template
from flask_json import FlaskJSON, as_json
from gameloop import GameLoop

game = GameLoop()
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
    names_scores = game.names_and_scores()
    return {'event': event, 'scores': names_scores}


@app.route("/statusNoWait")
@as_json
def status_nowait():
    names_scores = game.names_and_scores()
    return {'scores': names_scores}


app.run(host='localhost', threaded=True)
