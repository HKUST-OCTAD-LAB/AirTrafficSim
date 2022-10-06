# Getting started

## Running AirTrafficSim

You can run AirTrafficSim by executing the following commands in your console.

```{code-block} bash
conda activate airtrafficsim
cd AirTrafficSim
python -m airtrafficsim
```

If you are running AirTrafficSim for the first time, it will unpack the navigation data which will take a few minutes to complete. After executing the commands, you will see the following output in your console.

```{code-block} bash
Reading NAV data...
Running server at http://localhost:6111
```

```{note}
AirTrafficSim uses port 6111 for communication between client and server. Please open or forward the port accordingly if needed.
````

You should then be able to open the UI using any modern browser at <http://localhost:6111>. You will see the UI similar to below. 

```{image} images/UI.png
```

## Running AirTrafficSim without UI

You can also run AirTrafficSim without the UI by providing the name of an environment listed in `environments/`. The environment name should be identical to the file name.

```{code-block} bash
conda activate airtrafficsim
cd AirTrafficSim
python -m airtrafficsim --headless <environment name>
```

These commands will execute the specified simulation environment without running the UI. The output data will be stored in `result/` as a CSV file. More details will be discussed in the tutorial.
