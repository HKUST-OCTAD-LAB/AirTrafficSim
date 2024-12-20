"""
An entry point to the backend of AirTrafficSim.

Attributes:

app : Flask()
    A flask server object.
socketio : SocketIO()
    A SocketIO object for communication.

"""

from importlib import import_module
from pathlib import Path

from flask import Flask, render_template
from flask_socketio import SocketIO

from . import Czml
from .data import Data
from .replay import Replay, ReplayCategory, ReplayDir, ReplayMode

# TODO: use fastapi
app = Flask(
    __name__,
    static_url_path="",
    static_folder=Path(__file__).parent.parent.joinpath("data/client/build"),
    template_folder=str(
        Path(__file__).parent.parent.joinpath("data/client/build")
    ),
)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    max_http_buffer_size=1e8,
    ping_timeout=60,
    async_mode="eventlet",
    logger=True,
)  # engineio_logger=True


@socketio.on("connect")  # type: ignore
def test_connect() -> None:
    print("Client connected")


@socketio.on("disconnect")  # type: ignore
def test_disconnect() -> None:
    print("Client disconnected")


@socketio.on("getReplayDir")  # type: ignore
def get_replay_dir() -> ReplayDir:
    """Get the list of directories in data/replay"""
    return Replay.get_replay_dir()


@socketio.on("getReplayCZML")  # type: ignore
def get_replay_czml(replayCategory: ReplayCategory, replayFile: str) -> Czml:
    """
    Generate a CZML file to client for replaying data.

    Parameters
    ----------
    replayCategory : string
        The category to replay (historic / simulation)
    replayFile : string
        Name of the replay file directory

    Returns
    -------
    {}
        JSON dictionary of the CZML data file
    """
    return Replay.get_replay_czml(replayCategory, replayFile)


@socketio.on("getGraphHeader")  # type: ignore
def get_graph_header(
    mode: ReplayMode, replayCategory: ReplayCategory, replayFile: str
) -> list[str]:
    """
    Get the list of parameters name of a file suitable for plotting graph.

    Parameters
    ----------
    mode : string
        AirTrafficSim mode (replay / simulation)
    replayCategory : string
        The category to replay (historic / simulation)
    replayFile : string
        Name of the replay file directory

    Returns
    -------
    string[]
        List of graph headers
    """
    return Replay.get_graph_header(mode, replayCategory, replayFile)


@socketio.on("getGraphData")  # type: ignore
def get_graph_data(
    mode: ReplayMode,
    replayCategory: ReplayCategory,
    replayFile: str,
    simulationFile: str,
    graph: str,
) -> Czml:
    """
    Get the data for the selected parameters to plot a graph.

    Parameters
    ----------
    mode : string
        AirTrafficSim mode (replay / simulation)
    replayCategory : string
        The category to replay (historic / simulation)
    replayFile : string
        Name of the replay file directory

    Returns
    -------
    {}
        JSON file for graph data for Plotly.js
    """
    return Replay.get_graph_data(
        mode, replayCategory, replayFile, simulationFile, graph
    )


@socketio.on("getSimulationFile")  # type: ignore
def get_simulation_file() -> list[str]:
    """
    Get the list of files in airtrafficsim/env/

    Returns
    -------
    string[]
        List of simulation environment file names
    """
    simulation_list = []
    for file in sorted(
        Path(__file__).parent.parent.joinpath("data/environment/").glob("*.py")
    ):
        if file.name != "__init__.py":
            simulation_list.append(file.name.removesuffix(".py"))
    return simulation_list


@socketio.on("runSimulation")  # type: ignore
def run_simulation(file: str) -> None:
    """
    Start the simulation given file name.

    Parameters
    ----------
    file : string
        Environment file name
    """
    print(file)
    if file == "ConvertHistoricDemo":
        socketio.emit(
            "loadingMsg",
            "Converting historic data to simulation data... <br> "
            "Please check the terminal for progress.",
        )
    elif file == "WeatherDemo":
        socketio.emit(
            "loadingMsg",
            "Downloading weather data... <br> "
            "Please check the terminal for progress.",
        )
    else:
        socketio.emit(
            "loadingMsg",
            "Running simulation... <br> "
            "Please check the terminal for progress.",
        )
    socketio.sleep(0)
    Env = getattr(
        import_module("airtrafficsim.data.environment." + file, "..."), file
    )  # FIXME(abrah): not ideal.
    env = Env()
    env.run(socketio)


@socketio.on("getNav")  # type: ignore
def get_Nav(lat1: float, long1: float, lat2: float, long2: float) -> Czml:
    """
    Get the navigation waypoint data given

    Parameters
    ----------
    lat1 : float
        Latitude (South)
    long1 : float
        Longitude (West)
    lat2 : float
        Latitude (North)
    long2 : float
        Longitude (East)

    Returns
    -------
    {}
        JSON CZML file of navigation waypoint data
    """
    return Data.get_nav(lat1, long1, lat2, long2)


@socketio.on("getEra5Wind")  # type: ignore
def get_era5_wind(
    lat1: float, long1: float, lat2: float, long2: float, file: str, time: str
):
    """
    Get the ERA5 wind data image to client

    Parameters
    ----------
    lat1 : float
        Latitude (South)
    long1 : float
        Longitude (West)
    lat2 : float
        Latitude (North)
    long2 : float
        Longitude (East)

    Returns
    -------
    {}
        JSON CZML file of ERA5 wind data image
    """
    return Data.get_era5_wind(file, lat1, long1, lat2, long2, time)


@socketio.on("getEra5Rain")  # type: ignore
def get_era5_rain(
    lat1: float, long1: float, lat2: float, long2: float, file: str, time: str
) -> Czml:
    """
    Get the ERA5 rain data image to client

    Parameters
    ----------
    lat1 : float
        Latitude (South)
    long1 : float
        Longitude (West)
    lat2 : float
        Latitude (North)
    long2 : float
        Longitude (East)

    Returns
    -------
    {}
        JSON CZML file of ERA5 rain data image
    """
    return Data.get_era5_rain(file, lat1, long1, lat2, long2, time)


@socketio.on("getRadarImage")  # type: ignore
def get_radar_img(
    lat1: float, long1: float, lat2: float, long2: float, file: str, time: str
) -> Czml:
    """
    Get the radar data image to client

    Parameters
    ----------
    lat1 : float
        Latitude (South)
    long1 : float
        Longitude (West)
    lat2 : float
        Latitude (North)
    long2 : float
        Longitude (East)
    time : string
        Time in ISO format
    file : string
        File name of the radar image

    Returns
    -------
    {}
        JSON CZML file of radar data image
    """
    return Data.get_radar_img(file, lat1, long1, lat2, long2, time)


# TODO: check where is index.html
@app.route("/")
def serve_client() -> str:
    """Serve client folder to user"""
    return render_template("index.html")


def run_server(port: int = 6111, host: str = "127.0.0.1") -> None:
    # Change host to 0.0.0.0 during deployment
    """Start the backend server."""
    print(f"Running server at http://{host}:{port}")
    socketio.run(app, port=port, host=host)
