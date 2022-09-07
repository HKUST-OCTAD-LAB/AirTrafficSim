# Understanding the project structure

AirTrafficSim consists of 4 main folders including `airtrafficsim`, `data`, `client`, and `docs`. This page explains the purpose of each folders. To create a new simulation, you should create a new simulation environment file in `airtrafficsim/env/`. When a simulation is finished, the result will be saved to `data/replay/simulation`.

```{image} ../images/Project_structure.png
:width: 60%
:align: center
```

---

## airtrafficsim 📁

The airtrafficsim folder contains all Python files for air traffic simulation and data processing. It contains 4 folders and a `__main__.py` file which serves as the main entrance of the program.

### &emsp;env 📁

<ul>
The env folder stores different Python files to setup simulation environment. The creation of such file will be explained in [Creating a simulation environment](creating_env) page. Two sample files `DemoEnv.py` and `FullFlightDemo.py` are provided.
</ul>

### &emsp;core 📁

<ul>
The core folder contains the simulation code of AirTrafficSim. This includes `aircraft.py`, `traffic.py`, `autopilot.py`, `navigation.py`, `performance.py`, `bada.py`, `weather.py`, and `era5.py`.
</ul>

### &emsp;server 📁

<ul>
The server folder contains the server side programs of AirTrafficSim to serve the web-based UI to and communicate with client. It is written in Python with [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/index.html). This includes `server.py`, `data.py`, and `replay.py`.
</ul>

### &emsp;utils 📁

<ul>
The utils folder contains utility programs to assist simulation. This include `calculation.py`, `enums.py`, `unit_conversion.py`, and `route_detection.py`.
</ul>

---

## data 📁

The data folder contrains all the data needed for AirTrafficSim.

### &emsp;BADA 📁</ul>

<ul>
The BADA folder contains the BADA aircraft Performance data. The data is not included in the download but is obtainable at [eurocontrol](https://www.eurocontrol.int/model/bada) website. Please unzip and copy the data files into this folder.
</ul>

### &emsp;nav 📁

<ul>
The nav folder includes a navigation data at `data/nav/xplane_default_data.zip` obtained from [Xplane-11 data](https://developer.x-plane.com/docs/data-development-documentation/). The data will be extracted when AirTrafficSim is run for the first time.
</ul>

### &emsp;weather 📁

<ul>
The weather folder is empty by default. It servers as the directory to store ECMWF ERA5 data when you decided to use such data for simulation. It also stores user-provided radar image as high-resolution convective weather data. 
</ul>

### &emsp;replay 📁

<ul>
The replay folder stores the flight trajectories data. `replay/historic/` stores the user-provided historic data. A example data from FlightRadar24 is included. Please note that each data set should have its own folder.

`data/replay/simulation/` contains the output files from simulation. The data is stored in a folder with this naming convention `<Environment name>-<actual start time of simulation in UTC>`. In each folder, there is a master .csv file with the same name that include every flight in the simulation and multiple separate .csv files for each flight.
</ul>

---

## client 📁

The `client` folder contains the source and pre-compiled build of AirTrafficSim's UI. It is written in react.js with [Ionic Framework](https://ionicframework.com/). It contains a 3D globe using [Cesium.js + Cesium ion](https://cesium.com/) and [Resium](https://resium.reearth.io/). It also contains a graph UI component using [Plot.js](https://plotly.com/javascript/).

---

## docs 📁

The `docs` folder contains the documentation of AirTrafficSim built using [Sphinx](https://www.sphinx-doc.org/en/master/index.html) with [Furo](https://github.com/pradyunsg/furo) theme.
