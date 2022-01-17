# AirTrafficSim
Air traffic sim is a web-based air traffic simulation and visualization platform. Its goal is to provide a foundation to conduct air traffic management (ATM) research as well as to enable an easy-to-access UI for user to study the result.

## Project structure (To be updated)
```
AirTrafficSim/
│
├── client/
│   ├── src/
│   │   ├── pages/
│   │   ├── utils/
│   │   └── App.tsx
│   ├── .env
│   ├── .gitignore
│   ├── package.json
│   └── Dockerfile
│
├── server/
│   ├── src/
│   │   ├── models/
│   │   ├── routes/
│   │   └── database.js
│   ├── server.js
│   ├── .env
│   ├── .gitignore
│   ├── package.json
│   └── Dockerfile
│
├── simulation/
│   ├── atm/
│   │   └── __init.py
│   ├── data/
│   │   └── BADA/
│   ├── env/
│   │   ├── __init__.py
│   │   └── environment.py
│   ├── traffic/
│   │   ├── __init__.py
│   │   ├── aircraft.py
│   │   ├── performance.py
│   │   └── traffic.py
│   ├── __main__.py
│   └── .gitignore
│
├──doc/
│
├── docker-compose.yml
└── Readme.md
```
## client/
The client folder contains the UI of the website. It is written in react.js with [Material UI Library](https://mui.com/). It contains a 3D map using [Cesium.js + Cesium ion](https://cesium.com/) and [Resium](https://resium.reearth.io/).

Secret: .env file contains the access token to Cesium ion.
>REACT_APP_CESIUMION_ACCESS_TOKEN=

## server/
The server folder contains the server side program of the website. It is written in [nodejs](https://nodejs.org/en/) using [expressjs](https://expressjs.com/) and [socket.io](https://socket.io/). The platform is targeted to utilize MERN stack (MongoDB, Express JS, React JS and Node JS).
## simulation/
The simulation folder contains the python code for air traffic simulation. It contains 4 folders: [atm/](simulation/atm/), [data/](simulation/data/), [env/](simulation/env/), and [traffic/](simulation/traffic/) as well as \_\_main\_\_.py which is the main entrance of the program.

### [atm/](simulation/atm/)
The atm folder contains the simulation code for air traffic management (ATM) and air traffic controller (ATC). This will be the research focus to improve existing ATM strategies and algorithm.

### [data/](simulation/data/)
The data folder will contains all the necessary data to conduct the simulation. This includes:
- [x] Aircraft Performance data ([BADA 3.15](https://www.eurocontrol.int/model/bada))
- [ ] Navigation data (can extract VHHH data from [eAIP](https://www.ais.gov.hk/eaip_20211202/2021-12-02-000000/html/index-en-US.html))
- [ ] Weather data

### [env/](simulation/env/)
The environment folder contains the simulation setup for study.

### [traffic/](simulation/traffic/)
The traffic folder contains the air traffic simulation code. It is targeted to simulate multiple aircrafts' trajectories per timestep efficiently and accurately using BADA performance data as well as simulate aircraft' autopilot and navigation system. [performance.py](simulation/traffic/performance.py) contains the implementation of BADA performance data following BADA user menu. [traffic.py](simulation/traffic/traffic.py) contains the implementation of the base traffic array which contains all the state variables for all aircraft at one timestamp. [autopilot.py](simulation/traffic/autopilot.py) contains the implementation of aircraft autopilot and flight management system (which includes navigation, flight plan, etc.).

## System architecture
Initial system architecture plan: 
![](doc/images/System%20architecture.png)