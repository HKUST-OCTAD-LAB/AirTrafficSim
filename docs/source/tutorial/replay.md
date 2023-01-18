# Replaying data

AirTrafficSim allows you to replay historicaland simulated flight data. For historical flights, the data are stored in `data/flight_data`, while the data for simulated data are stored in `result/`. For the details of replay function, please refer to the API reference [airtrafficsim.server.replay](../api/server/airtrafficsim.server.replay).


## Replaying historical data

Historical data from with [FlightRadar24](https://www.flightradar24.com/) and [OpenSky format](https://opensky-network.org/) can be processed. A sample data with FlightRadar24 format is provided in `data/flight_data/2018-05-01/`. Note that each .csv file in the folder represents one flight. This is what the sample data looks like.


```{note}
Sometimes, there might be a problem to replay OpenSky data if the data size is too large, as the data frequency is quite high. Work is in progress to improve the handling of OpenSky data by integrating the [traffic](https://github.com/xoolive/traffic) library.
```

```{image} ../images/Replay_historic.png
```

## Replaying simulation data

The output of a simulation will be stored in a new folder in `result/` with the following format `<environment name>-<actual simulation start time in UTC>`. In each folder, there will be a master .csv file containing all flights in simulation with the same name.

To try it out, you can create one sample data by running `python -m airtrafficsim --headless DemoEnv`. You may find the sample data located similarly at `result/DemoEnv-2022-09-06T03:48:21/`. This is what the sample looks like.

```{tip}
When replaying simulation data, you can view the plot for different simulation parameters by using the "Show Graph" selector.
```

```{image} ../images/Replay_simulation.png
```
