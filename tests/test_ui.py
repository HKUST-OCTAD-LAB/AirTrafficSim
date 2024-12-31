from pathlib import Path

import pytest
from flask.testing import FlaskClient
from flask_socketio import SocketIOTestClient

import airtrafficsim.server.server as server


@pytest.fixture()
def app() -> FlaskClient:
    return server.app.test_client()


@pytest.fixture()
def client() -> SocketIOTestClient:
    return server.socketio.test_client(server.app)


def test_client(app: FlaskClient) -> None:
    response = app.get("/")
    assert response.data != ""
    # assert response.status_code == 200


def test_socketio(client: SocketIOTestClient) -> None:
    assert client.is_connected()


@pytest.mark.skip(reason="deprecated")
def test_get_nav(client: SocketIOTestClient) -> None:
    r = client.emit("getNav", -10, -10, 10, 10, callback=True)
    assert len(r) > 1


@pytest.mark.skip(reason="deprecated")
def test_get_era5_wind(client: SocketIOTestClient) -> None:
    r = client.emit(
        "getEra5Wind",
        -10,
        -10,
        10,
        10,
        "WeatherDemo",
        "2018-05-01T03:03:03",
        callback=True,
    )
    assert r[1]["rectangle"]["material"]["image"]["image"]["uri"] != ""


@pytest.mark.skip(reason="deprecated")
def test_get_era5_rain(client: SocketIOTestClient) -> None:
    r = client.emit(
        "getEra5Rain",
        10,
        10,
        20,
        20,
        "WeatherDemo",
        "2018-05-01T03:03:03",
        callback=True,
    )
    assert r[1]["rectangle"]["material"]["image"]["image"]["uri"] != ""


@pytest.mark.skip(reason="deprecated")
def test_get_radar_img(client: SocketIOTestClient) -> None:
    r = client.emit(
        "getRadarImage",
        15.0,
        110.0,
        25.0,
        120.0,
        "WeatherDemo",
        "2018-05-01T03:03:03",
        callback=True,
    )
    assert r[1]["rectangle"]["material"]["image"]["image"]["uri"] != ""


@pytest.mark.skip(reason="deprecated")
def test_get_replay_dir(client: SocketIOTestClient) -> None:
    r = client.emit("getReplayDir", callback=True)
    path = Path(__file__).parent.parent.joinpath("airtrafficsim/data/result")
    print(next(iter(path.glob("DemoEnv*"))).name)
    assert r == {
        "historic": ["2018-05-01"],
        "simulation": [
            next(iter(path.glob("WeatherDemo*"))).name,
            next(iter(path.glob("OpenApDemo*"))).name,
            next(iter(path.glob("FullFlightDemo*"))).name,
            next(iter(path.glob("DemoEnv*"))).name,
            next(iter(path.glob("ConvertHistoricDemo*"))).name,
        ],
        "simulation_files": {
            next(iter(path.glob("WeatherDemo*"))).name: [
                next(iter(path.glob("WeatherDemo*/WeatherDemo*.csv"))).name
            ],
            next(iter(path.glob("OpenApDemo*"))).name: [
                next(iter(path.glob("OpenApDemo*/OpenApDemo*.csv"))).name
            ],
            next(iter(path.glob("FullFlightDemo*"))).name: [
                next(
                    iter(path.glob("FullFlightDemo*/FullFlightDemo*.csv"))
                ).name
            ],
            next(iter(path.glob("DemoEnv*"))).name: [
                next(iter(path.glob("DemoEnv*/DemoEnv*.csv"))).name
            ],
            next(iter(path.glob("ConvertHistoricDemo*"))).name: [
                next(
                    iter(
                        path.glob(
                            "ConvertHistoricDemo*/ConvertHistoricDemo*.csv"
                        )
                    )
                ).name
            ],
        },
    }


@pytest.mark.skip(reason="deprecated")
def test_get_simulation_file(client: SocketIOTestClient) -> None:
    r = client.emit("getSimulationFile", callback=True)
    assert r == [
        "ConvertHistoricDemo",
        "DemoEnv",
        "FullFlightDemo",
        "OpenApDemo",
        "WeatherDemo",
    ]


@pytest.mark.skip(reason="deprecated")
def test_get_replay_czml(client: SocketIOTestClient) -> None:
    r = client.emit("getReplayCZML", "historic", "2018-05-01", callback=True)
    assert len(r) > 1


@pytest.mark.skip(reason="deprecated")
def test_get_graph_header(client: SocketIOTestClient) -> None:
    path = next(
        iter(
            Path(__file__)
            .parent.parent.joinpath("airtrafficsim/data/result")
            .glob("DemoEnv*")
        )
    )
    r = client.emit(
        "getGraphHeader",
        "replay",
        "simulation",
        path.name + "/" + next(iter(path.glob("DemoEnv*.csv"))).name,
        callback=True,
    )
    assert r == [
        "None",
        "alt",
        "cas",
        "tas",
        "mach",
        "vs",
        "heading",
        "bank_angle",
        "path_angle",
        "mass",
        "fuel_consumed",
        "thrust",
        "drag",
        "esf",
        "accel",
        "ap_track_angle",
        "ap_heading",
        "ap_alt",
        "ap_cas",
        "ap_mach",
        "ap_procedural_speed",
        "ap_wp_index",
        "ap_next_wp",
        "ap_dist_to_next_fix",
        "ap_holding_round",
        "flight_phase",
        "configuration",
        "speed_mode",
        "vertical_mode",
        "ap_speed_mode",
        "ap_lateral_mode",
        "ap_throttle_mode",
    ]


@pytest.mark.skip(reason="deprecated")
def test_get_graph_data(client: SocketIOTestClient) -> None:
    path = next(
        iter(
            Path(__file__)
            .parent.parent.joinpath("airtrafficsim/data/result")
            .glob("DemoEnv*")
        )
    )
    r = client.emit(
        "getGraphData",
        "replay",
        "simulation",
        path.name + "/" + next(iter(path.glob("DemoEnv*.csv"))).name,
        path.name + "/" + next(iter(path.glob("DemoEnv*.csv"))).name,
        "alt",
        callback=True,
    )
    assert len(r[0]["x"]) > 1 and len(r[0]["y"]) > 1


@pytest.mark.skip(reason="deprecated")
def test_run_simulation(client: SocketIOTestClient) -> None:
    client.emit("runSimulation", "DemoEnv")
    r = client.get_received()
    assert len(r) > 0
