from pathlib import Path
from flask import Flask, render_template
from flask_socketio import SocketIO
from server.replay import Replay
from env.environment import Environment
import eventlet

eventlet.monkey_patch()

app = Flask(__name__, static_url_path='', static_folder=Path(__file__).parent.parent.parent.joinpath('data/build'), template_folder=str(Path(__file__).parent.parent.parent.joinpath('data/build')))
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet', logger=True)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('getReplayDir')
def get_replay_dir():
    return Replay.get_replay_dir()

@socketio.on('getReplayCZML')
def get_replay_czml(category, date):
    return Replay.get_replay_czml(category, date)

@socketio.on('runSimulation')
def run_simulation():
    env = Environment()
    env.run()

@app.route("/")
def serve_client():
    return render_template("index.html")

def run_server(port = 5000):
    print("Running server at port", port)
    socketio.run(app, port=port)
