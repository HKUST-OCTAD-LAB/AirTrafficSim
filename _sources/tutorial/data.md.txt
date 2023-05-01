# Understanding the data folder

After initialising AirTrafficSim with `airtrafficsim --init <folder path>`, the `airtrafficsim_data/` alias folder is created at the user-specified location which links to the [`airtrafficsim/data/`](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/tree/main/airtrafficsim/data) folder. There are 7 folders inside to provide and save information from AirTrafficSim. This page will explain the purpose of these folders. 

To create a new simulation, you should create a new simulation environment file in `airtrafficsim_data/environment/` following the [Creating a simulation environment](./creating_env) guide. When a simulation is finished, the result will be saved to `airtrafficsim_data/result/`.

```{seealso}
If you want to understand the full project structure of AirTrafficSim, please visit [Understanding the project structure](../development/structure).
```

## airtrafficsim_data 📁

### &emsp;client 📁

<ul>

The client folder stores the pre-compiled build of AirTrafficSim's web client which is compressed in a zip file [`build.zip`](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/blob/main/airtrafficsim/data/client/build.zip). After using AirTrafficSim for the first time, the web client will be unzipped into the `airtrafficsim_data/client/build` folder for the AirTrafficSim's backend server to serve the client code to users to open in the browser.

</ul>

### &emsp;environment 📁

<ul>

The environment folder contains different Python files to set up the simulation environments. The creation of such a file will be explained on the [Creating a simulation environment](creating_env) page. Four sample tutorial files, including `DemoEnv.py`, `FullFlightDemo.py`, `WeatherDemo.py`, and `ConvertHistoricDemo.py`, are provided which are also explained in the tutorials [Creating a simulation environment](./creating_env), [Adding flight plan](./flight_plan), [Using weather database](./weather), and [Converting historical data](./historic) respectively.

</ul>

### &emsp;flight_data 📁

<ul>

The flight_data folder stores user-provided historical flight trajectory data. A sample data set of arrival flights to Hong Kong International Airport (VHHH) on 01 MAY 2018 from FlightRadar24 is included. To provide your own flight data, please open a folder and stores the CSV files with each CSV file representing each flight and named as its flight number. The CSV files should have a header with at least the following parameters to [replay the flights](./replay):

| Parameters | Details | Types |
| --- | --- | --- |
| timestamp | Unix/Epoch time in seconds (10-digit) | float |
| lat | Latitude (degree) | float |
| long | Longitude (degree) | float |
| alt | Altitude (meter) | float |
| gspeed | Ground speed (knot) | float|

Two additional parameters are needed for AirTrafficSim to convert the historical flight data to a simulation environment automatically as explained in [this tutorial](./historic.md).

| Parameters | Details | Types |
| --- | --- | --- |
| hangle | Heading angle (degree) | float |
| Aircraft_model | [ICAO Aircraft Type Designators](https://www.icao.int/publications/doc8643/pages/search.aspx) | string |

```{note}
Please note that each data set should have its own folder.
```

</ul>

### &emsp;navigation 📁

<ul>

The navigation folder includes navigation data at [`airtraffficsim_data/navigation/xplane_default_data.zip`](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/blob/main/airtrafficsim/data/navigation/xplane_default_data.zip) obtained from [Xplane-11 data](https://developer.x-plane.com/docs/data-development-documentation/). The data will be extracted into `airtraffficsim_data/navigation/xplane/` when AirTrafficSim is executed for the first time. It is used to provide the fix, nav aids, airways, airports, STARs, and SIDs information.

</ul>

### &emsp;performance 📁

<ul>

The performance folder is intended to contain any necessary data for different aircraft performance models. To use the BADA 3.15 performance model, the BADA aircraft Performance data should be extracted to the [`airtrafficsim/performance/BADA`](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim/tree/main/airtrafficsim/data/performance/BADA) folder. The data is not included during installation due to licensing requirements but it is obtainable at [eurocontrol](https://www.eurocontrol.int/model/bada) website.

</ul>

### &emsp;result 📁

<ul>

The result folder contains the output files from the simulation. The result of each simulation is stored in a folder with this naming convention `<Environment name>-<real world start time of simulation in UTC>`. In each folder, there is a master .csv file with the same name that includes every flight in the simulation.

</ul>

### &emsp;weather 📁

<ul>

The weather folder is empty by default. It serves as the directory to store ECMWF ERA5 data in `airtrafficsim_data/weather/era5` when you selected to download such data for simulation. It also stores user-provided radar images in `airtrafficsim_data/weather/radar` as high-resolution convective weather data. The provided radar images should be stored in a folder named after the environment name.

</ul>
