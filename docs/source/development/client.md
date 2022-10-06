# Client development

AirTrafficSim's web-based client is written with javascript using [React.js](https://reactjs.org/) framework. The UI components are created using [Ionic React](https://ionicframework.com/docs/react) library. The 3D globe and air traffic visualization are powered by [Cesium.js](https://cesium.com/) library and [Resium](https://resium.reearth.io/) while the graph is plotted using [Plotly.js](https://plotly.com/javascript/) library. The communication is handled with [Socket.IO](https://socket.io/) library.

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
Please also obtain a Cesium access token from  [Cesium ion portal](https://cesium.com/platform/cesium-ion/) after signing up for a free account and copy it into a new file `.env` in `client/` with the following line:

>REACT_APP_CESIUMION_ACCESS_TOKEN= \<Cesium Access Token\>

This allows the UI to properly stream and render the map, terrain, 3D building, and more.
```

## Developing client

The client code base are written in `client/src/pages/Simulation.tsx` with a React functional component called `Simulation`. The `client/src/utils/websocket.ts` file contains the setup of the Socket.IO WebSocket connection with the server's URL and port number.

To run the UI development environment:

```
cd AirTrafficSim/client/
yarn start
```

You should be able to open the development UI using any modern browser at http://localhost:3000. It will live-refresh once you make any changes to the UI. In addition, you may want to run the AirTrafficSim backend to run a simulation or generate a replay.

To run the AirTrafficSim backend, open a new terminal window and run a server instance:

```
cd AirTrafficSim/
conda activate airtrafficsim
python -m airtrafficsim
```

## Building client

After finishing building the client, you can build the UI by executing the following commands:

```
cd AirTrafficSim/client/
yarn build
```

You can then push and merge the client to the GitHub repository.