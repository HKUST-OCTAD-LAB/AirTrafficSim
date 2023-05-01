# Running a simulation

After setting up the simulation environment, you may run the simulation by either using the UI to select the simulation environment or by running AirTrafficSim in standalone mode with `airtrafficsim --headless <environment name>`. 

To run the simulation in the UI, click the `Simulation` button in the toolbar and select the environment in the popup menu.

```{image} ../images/Simulation_select.png
```

Then, the selected environment will be dynamically imported and initialised and the `def run(self):` function in its `Environment` base class will be executed to run the simulation for all timesteps specified. The data will be saved to `airtrafficsim_data/result`. 

This is what the UI will look like if you start the simulation using the UI. Note that there is a progress bar at the bottom to indicate the status of the simulation and the data will be sent to the UI every 0.5 seconds.


```{image} ../images/Simulation_UI.png
```

```{tip}
You can view the plot for different simulation parameters by using the "Show Graph" selector.
```
