# Understanding the project structure

## Architecture

AirTrafficSim is constructed with a frontend Javascript web client and a backend Python sever and simulation package. They communicate using WebSocket protocol on port 6111. AirTrafficSim read user-provided data in the `airtrafficsim_data/data` folder and the simulation results are exported as CSV files in the `airtrafficsim_data/result` folder.

```{image} ../images/Architecture.png
:width: 80%
:align: center
```

## File structure

There are 4 main folders including `airtrafficsim`, `client`, `docs` and `tests`. This page explains the purpose of each folder. Only the `airtrafficsim` folder is packaged in conda forge and downloaded when the user installs AirTrafficSim.

```{image} ../images/Project_structure.png
:width: 70%
:align: center
```

### airtrafficsim 📁

The airtrafficsim folder contains all Python source codes for air traffic simulation and data processing. It contains 3 folders and a `__main__.py` file which serves as the main entrance of the program.

#### &emsp;core 📁

<ul>

The core folder contains the simulation code of AirTrafficSim. This includes `aircraft.py` (a Python API interface to control each aircraft), `traffic.py` (main simulation loop and data array class), `autopilot.py`, `navigation.py`, `performance/performance.py` (main performance class), `performance/bada.py` (bada implementation class), `weather/weather.py` (main weather class), and `waether/era5.py` (era5 data implementation class).

</ul>

#### &emsp;server 📁

<ul>

The server folder contains the server-side programs of AirTrafficSim to serve the web-based UI and communicate with the client. It is written in Python with [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/index.html). This includes `server.py` (main entrance of the backend Flask server), `data.py`, and `replay.py`.

</ul>

#### &emsp;utils 📁

<ul>

The utils folder contains utility programs to assist with simulation. This includes `calculation.py`, `enums.py`, `unit_conversion.py`, and `route_detection.py`.

</ul>

---

### data 📁

The data folder contains all the data needed for AirTrafficSim. This includes the `client`, `environment`, `navigation`, `performance`, `weather`, `flight_data`, and `result` folders. Please follow the [Understanding the data folder](../tutorial/data.md) guide for the explanation of each folder inside.

---

### client 📁

The `client` folder contains the source code of AirTrafficSim's UI. It is written in react.js with [Ionic Framework](https://ionicframework.com/). It contains a 3D globe using [Cesium.js + Cesium ion](https://cesium.com/) and [Resium](https://resium.reearth.io/). It also contains a graph UI component using [Plot.js](https://plotly.com/javascript/). The main UI code is written in `client/src/pages/Simulation.tsx`.

---

### docs 📁

The `docs` folder contains the documentation of AirTrafficSim built using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) with [Furo](https://github.com/pradyunsg/furo) theme.
