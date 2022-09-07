# Creating simulation environment

To create a simulation environment, create a new file under [simulation/env](simulation/env/) with the name of the simulation. Then, create a subclass of `environment` in the file. You may refer to [DenoEnv.py](simulation/env/DemoEnv.py) as an example. Please note that the file name should be **exactly equal** to the class name including the capitals as it is used for the UI to select and refer the simulation environment.

Aircraft class in [aircraft.py](simulation/traffic/aircraft.py) represents an individual aircraft in traffic array and provides an interface to command the aircraft movement by simulating ATC. To control the aircraft, please write the algorithms in the override method `def atc_command(self):` in the `environment` subclass. You may refer to [DenoEnv.py](simulation/env/DemoEnv.py) as an example.

After setting up the environment and ATM algorithms, you may run the simulation by clicking the simulation buttom in the UI and selecting the simulation environment. Then, it will automatically execute `def run(self):` in `Environment` super class to run the simulation as specified. The data will be saved and visualized after the simulation.
