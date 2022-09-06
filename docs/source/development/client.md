# UI development

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