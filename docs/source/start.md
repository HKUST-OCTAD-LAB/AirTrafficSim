# Getting started

## Initialising AirTrafficSim

You should have initialised AirTrafficSim by following the [installation guide](./install.md) which will create a folder alias in your specified location called `airtrafficsim_data`. 

```bash
conda activate airtrafficsim
airtrafficsim -- init <path to a folder>
```

If you are running AirTrafficSim for the first time, it will unpack the navigation and web client data which will take a few minutes to complete.

```{attention}
Please ensure that BADA 3.15 data files are extracted in `airtrafficsim_data/performance/BADA/` and the API key for the weather database from ECMWF Climate Data Store is set up following [this guide](https://cds.climate.copernicus.eu/api-how-to).
```

## Running AirTrafficSim

You can run AirTrafficSim by executing the following commands in your console.

```bash
conda activate airtrafficsim
airtrafficsim
```

After executing the commands, you will see the following output in your console.

```{code-block} bash
Reading NAV data...
Running server at http://localhost:6111
```

```{note}
AirTrafficSim uses port 6111 for communication between the client and server. Please open or forward the port accordingly if needed.
```

You should then be able to open the UI using any modern browser at <http://localhost:6111>. You will see the UI similar to below. 

```{image} images/UI.png
```

```{note}
You may also check the console for any messages when running AirTrafficSim.
```

## Running AirTrafficSim without UI

You can also run AirTrafficSim without the UI by providing the name of an environment listed in `airtrafficsim_data/environment/`. The environment name should be identical to the file name.

```{code-block} bash
conda activate airtrafficsim
airtrafficsim --headless <environment name>
```

These commands will execute the specified simulation environment without running the UI. The output data will be stored in `airtrafficsim_result/` as a CSV file. More details will be discussed in the tutorial.
