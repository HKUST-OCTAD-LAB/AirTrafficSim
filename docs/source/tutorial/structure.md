# Project structure

## client/

The client folder contains the UI of the website. It is written in react.js with [Ionic Framework](https://ionicframework.com/). It contains a 3D map using [Cesium.js + Cesium ion](https://cesium.com/) and [Resium](https://resium.reearth.io/). It also contains graph plotting using [Recharts](https://recharts.org/en-US/).

## data/

The data folder contrains all the data needed for simulation.

- [x] BADA aircraft Performance data (Not included but obtainable at [eurocontrol](https://www.eurocontrol.int/model/bada) website.)
- [x] Navigation data at [xplane_default_data.zip](data/nav/xplane_default_data.zip) using [Xplane-11 data](https://developer.x-plane.com/docs/data-development-documentation/) under the terms of the Free Software Foundation General Public License (GPL).

[data/replay/historic/](data/replay/historic/) contains the historic data from FlightRadar24. A example is included. Please note that each data set should have its own folder.

[data/replay/simulation/](data/replay/simulation/) contains the output files from simulation. A example is included. The data is stroed in a folder and a master .csv file.


## simulation/

The simulation folder contains the python code for air traffic simulation. It contains 4 folders: [server/](simulation/server/), [atm/](simulation/atm/), [env/](simulation/env/), [traffic/](simulation/traffic/), and  [utils/](simulation/utils/) as well as [\_\_main\_\_.py](simulation/__main__.py) which is the main entrance of the program.

### [simulation/server/](simulation/server/)

The server folder contains the server side program of the website. It is written in Python with [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/index.html).
### [simulation/atm/](simulation/atm/)

The atm folder contains the simulation code for air traffic management (ATM) and air traffic controller (ATC). This will be the research focus to improve existing ATM strategies and algorithm.

### [simulation/env/](simulation/env/)

The environment folder contains the simulation setup for study.

### [simulation/traffic/](simulation/traffic/)

The traffic folder contains the air traffic simulation code. It is targeted to simulate multiple aircrafts' trajectories per timestep efficiently and accurately using BADA performance data as well as simulate aircraft' autopilot and navigation system. 

[traffic.py](simulation/traffic/traffic.py) contains the implementation of the base traffic array which contains all the state variables for all aircraft at one timestamp. 

[aircraft.py](simulation/traffic/aircraft.py) contains the class-like implementation of one individual aircraft. 

[performance.py](simulation/traffic/performance.py) contains the implementation of BADA performance data following BADA user menu. 

[autopilot.py](simulation/traffic/autopilot.py) contains the implementation of aircraft autopilot and flight management system (which includes navigation, flight plan, etc.). 

[weather.py](simulation/traffic/weather.py) contains implementation of weather for each aircraft.