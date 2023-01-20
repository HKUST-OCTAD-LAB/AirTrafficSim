# Installation

Conda environment is required to set up AirTrafficSim. First, download AirTrafficSim from GitHub and set up the conda environment by following commands:

```{code-block} bash
git clone https://github.com/HKUST-OCTAD-LAB/AirTrafficSim.git
cd AirTrafficSim
conda env create -f environment.yml
```

This will create a new conda enviornment called `airtrafficsim` and install all necessary dependencies. The web-based client has been pre-compiled and is ready to use directly after download.

```{attention}

After installation, please also download and unzip the [BADA data](https://www.eurocontrol.int/model/bada) in `data/BADA`. You will need to follow the instructions to request a license. In addition, please follow [this guide](https://cds.climate.copernicus.eu/api-how-to) to set up the API key for the weather database from ECMWF Climate Data Store.
```

Then, activate the environment each time you want to use AirTrafficSim.

```{code-block} bash
conda activate airtrafficsim
```

## Updating AirTrafficSim

You can update AirTrafficSim with the newest changes by executing the following command.

``` bash
git pull
```

```{tip}
You may git commit and/or push your local changes first before pulling new remote changes to avoid overwriting your changes.
```
