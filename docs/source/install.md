# Installation

AirTrafficsim uses conda for Python environment management. Linux or [WSL on window](https://learn.microsoft.com/en-us/windows/wsl/) is recommended for AirTrafficSim. While Windows and macOS should work, they are not tested. 

The latest stable release of AirTrafficSim can be installed from conda-forge. All dependencies will be installed automatically with the web client pre-built and ready for use directly after installation.

It is recommended to install AirTrafficSim in a new conda environment:

```bash
conda create -n airtrafficsim -c conda-forge airtrafficsim 
```

Then, please initialise AirTrafficSim by specifying a folder path to create a symbolic link to the [airtrafficsim_data](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/tree/main/airtrafficsim/data) folder:

```bash
conda activate airtrafficsim
airtrafficsim -- init <path to a folder>
```
This will allow you to provide or retrieve any data and create simulation environments for AirTrafficSim through this folder alias. Please visit the [documentation](https://hkust-octad-lab.github.io/AirTrafficSim/index.html) for more information.

```{attention}

After installation, please also download, unzip, and store BADA 3.15 data files in `airtrafficsim_data/performance/BADA/`. You will need to follow the instructions to request a license. In addition, please follow [this guide](https://cds.climate.copernicus.eu/api-how-to) to set up the API key for the weather database from ECMWF Climate Data Store.
```

Please be reminded to activate the environment each time you want to use AirTrafficSim:

```bash
conda activate airtrafficsim
```


```{seealso}
To install AirTrafficSim for development, please visit [Development guide](./development/guide).
```

## Updating AirTrafficSim

You can update AirTrafficSim with the newest changes by executing the following command.

``` bash
conda activate airtrafficsim
conda update -c conda-forge airtrafficsim 
```