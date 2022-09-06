# Installation

## AirTrafficSim

Conda environment is required to setup AirTrafficSim. First download AirTrafficSim from GitHub and setup conda environment by following commands:

```{code-block} bash
git clone https://github.com/HKUST-OCTAD-LAB/AirTrafficSim.git
conda env create -f environment.yml
```

This will install all necessary dependencies. The client has been pre-compile and is ready to use after download.

```{important}

After installation, please also download and unzip the [BADA data](https://www.eurocontrol.int/model/bada) in `data/BADA`. In addition, please follow [this guide](https://cds.climate.copernicus.eu/api-how-to) to setup the API key for the weather database from ECMWF Climate Data Store.
```

Then, activate the environment each time you want to use AirTrafficSim.

```{code-block} bash
conda activate airtrafficsim
```

---

## Client

If you want to contribute to the development of the client UI, please install [Nodejs](https://nodejs.org/en/) into the environment. You may also use your own nodejs install. Then, please also install [Yarn](https://classic.yarnpkg.com/en/) a package manager for Node.js.

```{code-block} bash
conda activate airtrafficsim
conda install -c conda-forge nodejs
npm install --global yarn
```

To install all the Node.js dependencies for client development, execute the following commands:

```{code-block} bash
conda activate airtrafficsim
cd AirTrafficSim/client/
yarn
```

```{important}
Please also obtain a Cesium access token from  [Cesium ion portal](https://cesium.com/platform/cesium-ion/) after signing up a free account and copy it into a new file `.env` in `client/` with the following line:
>REACT_APP_CESIUMION_ACCESS_TOKEN= \<Cesium Access Token\>
```

## Documentation

To contribute to the development of the documentation, please setup the environment with following commands. This will install [Sphinx](https://www.sphinx-doc.org/en/master/index.html) and related theme and library for this project.

```{code-block} bash
conda activate airtrafficsim
conda install -c conda-forge sphinx myst-parser furo numpydoc
```