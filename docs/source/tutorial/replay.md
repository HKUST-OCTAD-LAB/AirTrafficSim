# Replaying data

AirTrafficSim allows you to replay historic and simulated flight data. The data should be stored in `data/replay/`. For historic flight, the data are stored in `data/replay/historic`, while the data for simulated data are stored in `data/replay/simulation`. For the details of replay function, please refer to the API reference [airtrafficsim.server.replay](../api/server/airtrafficsim.server.replay).


## Replaying historic data

Historic data from with [FlightRadar24](https://www.flightradar24.com/) and [OpenSky format](https://opensky-network.org/) can be processed. A sample data with FlightRadar24 format is provided in `replay/historic/20180601/`. Note that each .csv file in the folder represent one flight. This is what the sample data looks like.


```{note}
Sometimes, there might be problem to replay OpenSky data if the data size is too large as the data frequency is quite high. Work is in progress to improve handling of OpenSky data by intergrating the [traffic](https://github.com/xoolive/traffic) library.
```

```{image} ../images/Replay_historic.png
```

## Replaying simulation data

The output of a simulation will be stored in a new folder in`replay/simulation/` with the following format `<environment name>-<actual simulation start time in UTC>`. In each folder, there will be a master .csv file contaning all flight in simulation with the same name. There will also be separated .csv files for each flight named by their callsign. You can select which file to replay.

You can create one sample by running `python -m airtrafficsim --headless DemoEnv`. You may find the sample data located similarly at `replay/simulation/DemoEnv-2022-09-06T03:48:21/`. This is what the sample data looks like.

```{tip}
When replaying simulation data, you can graph different parameters you want by using the "Show Graph" selector.
```

```{image} ../images/Replay_simulation.png
```
