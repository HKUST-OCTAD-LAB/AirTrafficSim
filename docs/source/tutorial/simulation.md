# Running a simulation

After setting up the simulation environment, you may run the simulation by either using the UI to select the simulation environment or by running AirTrafficSim without the UI with `python -m airtrafficsim --headless <environment name>`. 

```{image} ../images/Simulation_select.png
```

Then, the selected environment will be dynamically imported and initialized and the `def run(self):` function in its `Environment` super class will be executed to run simulation for all timesteps. The data will be saved to `data/replay/simulation/`. 

This is what the UI will looks like if the you start the simulation using the UI. Note that there is a progress bar at the bottom to indicate the status of the simulation and the data will be sent to the UI every 1 second.


```{image} ../images/Simulation_UI.png
```
