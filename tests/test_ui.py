from gc import callbacks
import pytest
from pathlib import Path
import airtrafficsim.server.server as server

@pytest.fixture()
def app():
    return server.app.test_client()

@pytest.fixture()
def client():
    return server.socketio.test_client(server.app)

def test_client(app):
    response = app.get('/')
    assert response.data != ''
    # assert response.status_code == 200

def test_socketio(client):
    assert client.is_connected()

def test_get_nav(client):
    r = client.emit('getNav', -10, -10, 10, 10, callback=True)
    assert len(r) > 1

def test_get_era5_wind(client):
    r = client.emit('getEra5Wind', -10, -10, 10, 10, 'WeatherDemo', '2018-05-01T03:03:03', callback=True)
    assert r[1]["rectangle"]["material"]["image"]["image"]["uri"] != ''

def test_get_era5_rain(client):
    r = client.emit('getEra5Rain', 10, 10, 20, 20, 'WeatherDemo', '2018-05-01T03:03:03', callback=True)
    assert r[1]["rectangle"]["material"]["image"]["image"]["uri"] != ''

def test_get_radar_img(client):
    r = client.emit('getRadarImage', 15.0, 110.0, 25.0, 120.0, 'WeatherDemo', '2018-05-01T03:03:03', callback=True)
    assert r[1]["rectangle"]["material"]["image"]["image"]["uri"] != ''

def test_get_replay_dir(client):
    r = client.emit('getReplayDir', callback=True)
    path = Path(__file__).parent.parent.joinpath('airtrafficsim/data/result')
    print(list(path.glob('DemoEnv*'))[0].name)
    assert r == {'historic': ['2018-05-01'], 
                 'simulation': [list(path.glob('WeatherDemo*'))[0].name,
                                list(path.glob('OpenApDemo*'))[0].name,
                                list(path.glob('FullFlightDemo*'))[0].name,
                                list(path.glob('DemoEnv*'))[0].name,
                                list(path.glob('ConvertHistoricDemo*'))[0].name],
                 'simulation_files': {list(path.glob('WeatherDemo*'))[0].name : [list(path.glob('WeatherDemo*/WeatherDemo*.csv'))[0].name],
                                     list(path.glob('OpenApDemo*'))[0].name : [list(path.glob('OpenApDemo*/OpenApDemo*.csv'))[0].name],
                                     list(path.glob('FullFlightDemo*'))[0].name : [list(path.glob('FullFlightDemo*/FullFlightDemo*.csv'))[0].name],
                                     list(path.glob('DemoEnv*'))[0].name : [list(path.glob('DemoEnv*/DemoEnv*.csv'))[0].name],
                                     list(path.glob('ConvertHistoricDemo*'))[0].name : [list(path.glob('ConvertHistoricDemo*/ConvertHistoricDemo*.csv'))[0].name]}}
                                      

def test_get_simulation_file(client):
    r = client.emit('getSimulationFile', callback=True)
    print(r)
    assert r == ['ConvertHistoricDemo', 'DemoEnv', 'FullFlightDemo', 'OpenApDemo', 'WeatherDemo']

def test_get_replay_czml(client):
    r = client.emit('getReplayCZML', 'historic', '2018-05-01', callback=True)
    assert len(r) > 1

def test_get_graph_header(client):
    path = list(Path(__file__).parent.parent.joinpath('airtrafficsim/data/result').glob('DemoEnv*'))[0]
    r = client.emit('getGraphHeader', 'replay', 'simulation', path.name+'/'+list(path.glob('DemoEnv*.csv'))[0].name, callback=True)
    assert r == ['None', 'alt', 'cas', 'tas', 'mach', 'vs',
                'heading', 'bank_angle', 'path_angle',
                'mass', 'fuel_consumed',
                'thrust', 'drag', 'esf', 'accel',
                'ap_track_angle', 'ap_heading', 'ap_alt', 'ap_cas', 'ap_mach', 'ap_procedural_speed',
                'ap_wp_index', 'ap_next_wp', 'ap_dist_to_next_fix', 'ap_holding_round',
                'flight_phase', 'configuration', 'speed_mode', 'vertical_mode', 'ap_speed_mode', 'ap_lateral_mode', 'ap_throttle_mode']
                                                    
def test_get_graph_data(client):
    path = list(Path(__file__).parent.parent.joinpath('airtrafficsim/data/result').glob('DemoEnv*'))[0]
    r = client.emit('getGraphData', 'replay', 'simulation', path.name+'/'+list(path.glob('DemoEnv*.csv'))[0].name, path.name+'/'+list(path.glob('DemoEnv*.csv'))[0].name, 'alt', callback=True)
    assert len(r[0]['x']) > 1 and len(r[0]['y']) > 1

def test_run_simulation(client):
    client.emit('runSimulation', 'DemoEnv')
    r = client.get_received()
    assert len(r) > 0
