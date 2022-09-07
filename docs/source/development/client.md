# Client development

## Installation

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

```{attention}
Please also obtain a Cesium access token from  [Cesium ion portal](https://cesium.com/platform/cesium-ion/) after signing up a free account and copy it into a new file `.env` in `client/` with the following line:

>REACT_APP_CESIUMION_ACCESS_TOKEN= \<Cesium Access Token\>

This allows the UI to properly stream and render the map, terrain, 3D building, and more.
```

## Others
To develop the UI, nodejs (tested with 16.13.0) and yarn is needed. Currently, the client uses port 3000 and the server uses port 5000 for communication. Please open or forward the ports accordingly if needed. 

To install the development environment: 

```
cd AirTrafficSim/client/
yarn
```

Please also extract a Cesium access token from  [Cesium ion portal](https://cesium.com/platform/cesium-ion/) after signing up a free account and copy it into a new file `.env` in `client/` as follow:
>REACT_APP_CESIUMION_ACCESS_TOKEN=

To run the UI development environment:

```
cd AirTrafficSim/client/
yarn start
```

Open a new terminal windows and run a server instance:

```
cd AirTrafficSim/
python simulation run
```

You should be able to open the UI using any modern browser at http://localhost:3000.

To build the UI after development:

```
cd AirTrafficSim/client/
yarn build
```