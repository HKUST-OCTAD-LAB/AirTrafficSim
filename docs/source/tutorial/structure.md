# Understanding the project structure

## Architecture

AirTrafficSim consists of a frontend Javascript client and a backend Python sever and simulation program. They communicate using WebSocket protocol on port 6111.

```{image} ../images/Architecture.png
:width: 80%
:align: center
```

## File structure

AirTrafficSim consists of 4 main folders including `airtrafficsim`, `client`, `data`, `docs`, `environments`, and `result`. This page explains the purpose of each folder. To create a new simulation, you should create a new simulation environment file in `environments/`. When a simulation is finished, the result will be saved to `result/`.

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

The server folder contains the server-side programs of AirTrafficSim to serve the web-based UI and communicate with the client. It is written in Python with [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/index.html). This includes `server.py`, `data.py`, and `replay.py`.

</ul>

#### &emsp;utils 📁

<ul>

The utils folder contains utility programs to assist simulation. This include `calculation.py`, `enums.py`, `unit_conversion.py`, and `route_detection.py`.

</ul>

---

### data 📁

The data folder contains all the data needed for AirTrafficSim.

#### &emsp;client 📁

<ul>

The client folder stores the pre-compiled build of AirTrafficSim's UI. It is used for AirTrafficSim to serve the client code to users.

</ul>

#### &emsp;flight_data 📁

<ul>

The flight_data folder stores user-provided historical flight trajectory data. An example of a data set from FlightRadar24 is included. Please note that each data set should have its own folder.

</ul>

#### &emsp;performance 📁

<ul>

The performance folder is intended to contain any necessary data for different performance models. The performance/BADA folder contains the BADA aircraft Performance data. The data is not included in the download but is obtainable at [eurocontrol](https://www.eurocontrol.int/model/bada) website. Please unzip and copy the data files into this folder.

</ul>

#### &emsp;navigation 📁

<ul>

The navigation folder includes navigation data at `data/navigation/xplane_default_data.zip` obtained from [Xplane-11 data](https://developer.x-plane.com/docs/data-development-documentation/). The data will be extracted when AirTrafficSim is run for the first time.

</ul>

#### &emsp;weather 📁

<ul>

The weather folder is empty by default. It serves as the directory to store ECMWF ERA5 data when you decided to use such data for simulation. It also stores user-provided radar images as high-resolution convective weather data. The folders are named after the environment name.

</ul>

---

### client 📁

The `client` folder contains the source code of AirTrafficSim's UI. It is written in react.js with [Ionic Framework](https://ionicframework.com/). It contains a 3D globe using [Cesium.js + Cesium ion](https://cesium.com/) and [Resium](https://resium.reearth.io/). It also contains a graph UI component using [Plot.js](https://plotly.com/javascript/).

---

### docs 📁

The `docs` folder contains the documentation of AirTrafficSim built using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) with [Furo](https://github.com/pradyunsg/furo) theme.

---

### environment 📁

The environment folder stores different Python files to set up the simulation environment. The creation of such a file will be explained on the [Creating a simulation environment](creating_env) page. Four sample tutorial files, including `DemoEnv.py`, `FullFlightDemo.py`, `WeatherDemo.py`, and `ConvertHistoricDemo.py`, are provided.

---

### result 📁

The result folder contains the output files from the simulation. The data is stored in a folder with this naming convention `<Environment name>-<actual start time of simulation in UTC>`. In each folder, there is a master .csv file with the same name that includes every flight in the simulation.