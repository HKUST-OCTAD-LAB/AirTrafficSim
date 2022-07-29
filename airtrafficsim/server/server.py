from pathlib import Path
from importlib import import_module
from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet

from airtrafficsim.server.replay import Replay
from airtrafficsim.server.data import Data

# eventlet.monkey_patch()

app = Flask(__name__, static_url_path='', static_folder=Path(__file__).parent.parent.parent.joinpath('client/build'), template_folder=str(Path(__file__).parent.parent.parent.joinpath('client/build')))
socketio = SocketIO(app, cors_allowed_origins='*', max_http_buffer_size=1e8, ping_timeout=60, async_mode='eventlet', logger=True) #engineio_logger=True 

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
def get_replay_czml(replayCategory, replayFile):
    return Replay.get_replay_czml(replayCategory, replayFile)

@socketio.on('getGraphHeader')
def get_graph_header(mode, replayCategory, replayFile):
    return Replay.get_graph_header(mode, replayCategory, replayFile)

@socketio.on('getGraphData')
def get_graph_data(mode, replayCategory, replayFile, simulationFile, graph):
    return Replay.get_graph_data(mode, replayCategory, replayFile, simulationFile, graph)

@socketio.on('getSimulationFile')
def get_simulation_file():
    simulation_list=[]
    for file in Path(__file__).parent.parent.joinpath('env/').glob('*.py'):
        if file.name != 'environment.py' and file.name != '__init__.py':
            simulation_list.append(file.name.removesuffix('.py'))
    return simulation_list

@socketio.on('runSimulation')
def run_simulation(file):
    Env = getattr(import_module('env.'+file), file)
    env = Env()
    env.run(socketio)

@socketio.on('getNav')
def get_Nav(lat1, long1, lat2, long2):
    return Data.get_nav(lat1, long1, lat2, long2)

@socketio.on('getEra5Wind')
def get_era5_wind(lat1, long1, lat2, long2, file):
    return Data.get_era5_wind(lat1, long1, lat2, long2, file)

@socketio.on('getEra5Rain')
def get_era5_rain(lat1, long1, lat2, long2, file):
    return Data.get_era5_rain(lat1, long1, lat2, long2, file)

@socketio.on('getRadarImage')
def get_radar_img(lat1, long1, lat2, long2, file):
    return Data.get_radar_img(lat1, long1, lat2, long2, file)

@app.route("/")
def serve_client():
    return render_template("index.html")

def run_server(port = 6111):
    print("Running server at http://localhost:"+str(port))
    socketio.run(app, port=port)
