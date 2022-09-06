# Getting started

### Running AirTrafficSim

You can run AirTrafficSim by executing the following commands. It uses port 6111 for communicaiton. Please open or forward the port accordingly if needed.

```{code-block} bash
conda activate airtrafficsim
cd AirTrafficSim
python -m airtrafficsim
```

You should be able to open the UI using any modern browser at <http://localhost:6111>.

You can also run AirTrafficSim without the UI by providing the name of an environment listed in `airtrafficsim/env`. The environment name should be identical to the file name.

```{code-block} bash
conda activate airtrafficsim
cd AirTrafficSim
python -m airtrafficsim --headless <environment name>
```

This will run the simulation without the UI with the specified environment. The output data will be stored in `data/simulation` as a CSV file.


## Creating simulation environment

To create a simulation environment, create a new file under [simulation/env](simulation/env/) with the name of the simulation. Then, create a subclass of `environment` in the file. You may refer to [DenoEnv.py](simulation/env/DemoEnv.py) as an example. Please note that the file name should be **exactly equal** to the class name including the capitals as it is used for the UI to select and refer the simulation environment.

Aircraft class in [aircraft.py](simulation/traffic/aircraft.py) represents an individual aircraft in traffic array and provides an interface to command the aircraft movement by simulating ATC. To control the aircraft, please write the algorithms in the override method `def atc_command(self):` in the `environment` subclass. You may refer to [DenoEnv.py](simulation/env/DemoEnv.py) as an example.

After setting up the environment and ATM algorithms, you may run the simulation by clicking the simulation buttom in the UI and selecting the simulation environment. Then, it will automatically execute `def run(self):` in `Environment` super class to run the simulation as specified. The data will be saved and visualized after the simulation.
