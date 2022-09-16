# AirTrafficSim

AirTrafficSim is a web-based air traffic simulation software written in Python and javascript. It is designed to visualize historic and research data, perform microscopic studies of air traffic movement with the integration of a historic weather database, and evaluate the performance of ATM algorithms.

## Features

- Replay histortic flights given data (FlightRadar 24 and simulated flights)
- Air traffic simulation using [BADA performance data](https://www.eurocontrol.int/model/bada) and OpenAP (WIP)
- Navigation data simulation and visualization from [x-plane 11](https://developer.x-plane.com/docs/data-development-documentation/)
- Autopilot and Flight Management System simulation
- Holding, vectoring, direct to maneuvers simulated
- Weather data from [ECMWF ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview) and custom radar image
- Air traffic is controlled with API interface to simulate ATC interaction

![AirTrafficSim](docs/source/images/UI_features.png)


## Credits

If you find AirTrafficSim useful for your research, please cite it as.

## Installation

Conda environment is required to setup AirTrafficSim. All dependencies will be installated automatically and the client has been pre-built and is ready for use after download.

To download, enter the following command:

```
git clone https://github.com/HKUST-OCTAD-LAB/AirTrafficSim.git
conda env create -f environment.yml
```

After installation, please also download, unzip, and store BADA data in [data/BADA](data/BADA/). In addition follow [this guide](https://cds.climate.copernicus.eu/api-how-to) to setup the API key for the weather database from ECMWF Climate Data Store.


## Running AirTrafficSim

You can run AirTrafficSim by executing the following commands. It uses port 6111 for communicaiton. Please open or forward the port accordingly if needed.

```
cd AirTrafficSim
conda activate airtrafficsim
python -m airtrafficsim
```

You should be able to open the UI using any modern browser at http://localhost:6111.


You can also run AirTrafficSim without the UI by providing the name of an environment which is listed in [airtrafficsim/env](airtrafficsim/env/). The environment name should be identical to the file name.

```
cd AirTrafficSim
conda activate airtrafficsim
python -m airtrafficsim --headless <environment name>
```

## Documentation

The detailed documentation for AirTrafficSim is available at xxx.

## Contribution

AirTrafficSim is under active development. We welcome everyone intersted to contribute to the project and make AirTrafficSim more feature-rich. Please feel free to raise any feature suggestion or bugs in the Issues board. Please also feel free to create any pull requests.