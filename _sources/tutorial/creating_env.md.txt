# Creating a simulation environment

The simulation environment files, located at `environments/`, tell AirTrafficSim how to initiate the environment and how to control the traffic during simulation. Four sample tutorial environments `DemoEnv`, `FullFlightDemo`, `WeatherDemo`, and `ConvertHistoricDemo` are included in `environments/`.

## Creating the file


```{tip}
It may be easier to copy one of the sample environments when creating a new one.
```

To create a simulation environment, create a new Python file under `environments/` with the name you want. Then, create a new Python class in the file with the same name. Note that this new class is actually a subclass of [airtrafficsim.core.environment](../api/core/airtrafficsim.core.environment).

```{important}
Please note that the file name should be **exactly equal** to the class name including the capitals as it is dynamically imported at runtime by Python when a user selects the environment in the UI.
```

## Creating the class content

We will discuss the setup of an environment file referencing `DemoEnv.py`. Notice that `class DemoEnv(Environment):` is a subclass of `Environment` at [airtrafficsim.core.environment](../api/core/airtrafficsim.core.environment).

```{code-block} python
from datetime import datetime
from pathlib import Path

from airtrafficsim.core.environment import Environment
from airtrafficsim.core.aircraft import Aircraft
from airtrafficsim.utils.enums import Config, FlightPhase

class DemoEnv(Environment):

    def __init__(self):
        # Section 1
        # Initialize environment base class
        super().__init__(file_name = Path(__file__).name.removesuffix('.py'), #File name (do not change)
                        start_time = datetime.fromisoformat('2022-03-22T00:00:00+00:00'),
                        end_time = 1000,
                        weather_mode = "",
                        performance_mode = "BADA" 
                        )

        # Section 2
        # Add aircraft
        self.aircraft_head = Aircraft(self.traffic, call_sign="HEAD", aircraft_type="A20N", flight_phase=FlightPhase.CRUISE, configuration=Config.CLEAN,
                                      lat=22.019213, long=113.539164, alt=20000.0, heading=175.0, cas=250.0, fuel_weight=10000.0, payload_weight=12000.0,
                                      arrival_airport="VHHH", arrival_runway="07R", star = "SIER7A", approach = "I07R", cruise_alt=37000)
        # self.aircraft_head.set_speed(250.0) # To set the aircraft to follow given speed command instead of auto procedural
        self.aircraft_fol = Aircraft(self.traffic, call_sign="FOLLOW", aircraft_type="A20N", flight_phase=FlightPhase.CRUISE, configuration=Config.CLEAN,
                                     lat=21.9, long=113.5, alt=20000.0, heading=175.0, cas=310.0, fuel_weight=10000.0, payload_weight=12000.0, cruise_alt=37000)


    # Section 3
    def should_end(self):
        return False

    # Section 4
    def atc_command(self):
        # User algorithm
        if self.global_time == 10:  
            # Right
            self.aircraft_fol.set_heading(220)
            # Left
            # self.aircraft_head.set_heading(150)

        if self.global_time == 300:
            # Climb
            self.aircraft_fol.set_alt(30000)
            # Descend
            # self.aircraft_head.set_alt(11000)

        if self.global_time == 900:
            self.traffic.del_aircraft(self.aircraft_head.index)
```

### 1. Initialize environment base class

There are five parameters needed to initialize the basic information of this simulation, which will be explained below.

1. `file_name` is used to name the solution files. It has been set by default. Please do not change.
2. `start_time` is a Python datetime object representing the **simulation UTC start time** that you want to study. It will be used to search for historical weather data. 
3. `end_time` is an interger value representing how many **seconds** you want the simulation to continue.
4. `weather_mode` is a string to select what **weather database** will be downloaded and used. ("": ISA, "ERA5": [ECMWF ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview))
5. `performance_mode` is a string to select which performance model is used. ("BADA": [BADA](https://www.eurocontrol.int/model/bada))
   
```{note}
We are working toward including [OpenAP](https://github.com/TUDelft-CNS-ATM/openap) performance data. Right now, only the BADA performance model can be used.
```

### 2. Add aircraft

Air traffic are stored in arrays at `Traffic` class in [airtrafficsim/core/traffic.py](../api/core/airtrafficsim.core.traffic). Each `Aircraft` in [airtrafficsim/core/aircraft.py](../api/core/airtrafficsim.core.aircraft) represents an individual aircraft in the traffic array and provides an interface to command the aircraft movement. The parameters to initialize an aircraft are explained below.

| Parameters | Meanings |
| :--------: | :------: |
| traffic | This points to the traffic array class. (The value must be `self.traffic`) |
| **General:** |
| call_sign | Call sign of the aircraft (string) |
| aircraft_type | ICAO aircraft type (string) |
| flight_phase | Current flight phase ([FlightPhase enums](../api/utils/airtrafficsim.utils.enums)) |
| configuration | Current configuration ([Configuration enums](../api/utils/airtrafficsim.utils.enums)) |
| **Position:** |
| lat | Current latitude (degree) |
| long | Current longitude (degree) |
| alt | Current altitude (feet) |
| cas | Current calibrated airspeed (knots) |
| **Weight:** |
| fuel_weight | Current fuel weight (kg) |
| payload_weight | Current payload weight (kg) |
| **Flight plan:** |
| departure_airport | OPTIONAL: Departure airport (string) |
| departure_runway | OPTIONAL: Departure runway (string) |
| sid | OPTIONAL: Standard Instrument Departure Procedure (string) |
| arrival_airport | OPTIONAL: Arrival airport (string) |
| arrival_runway | OPTIONAL: Arrival airport (string) |
| star   | OPTIONAL: Standard Terminal Arrival Procedure (string) |
| approach | OPTIONAL: ILS approach procedure (string) |
| flight_plan | OPTIONAL: Array of waypoints that the aircraft will fly ([string]) |
| cruise_alt | OPTIONAL: Cruise altitude (feet) |

### 3. Should end

This is an override function for the `Environment` base class to allow you to control whether the simulation should end earlier than indicated by `end_time`. For each timestep, AirTrafficSim will check the condition that the function returns. If it returns `True`, the simulation will end.

### 4. ATC command

This is an override function for the `Environment` base class to allow you to command how traffic move in this timestep. It can be a simple time-based condition in this sample or it can be a more complicated algorithm developed by you.