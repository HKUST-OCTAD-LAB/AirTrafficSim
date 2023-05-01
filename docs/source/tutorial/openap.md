# Uisng OpenAP performance model

Apart from the default [BADA 3.15 performance data](https://www.eurocontrol.int/model/bada), AirTrafficSim also support using the open-source [OpenAP](https://github.com/TUDelft-CNS-ATM/openap) performance model. This allows users to run AirTrafficSim without the need to obtain the licensed BADA 3.15 model. The `OpenApDemo` class in `airtrafficsim_demo/environment/OpenApDemo.py` provides a sample to set up such an environment.

```{note}
The support for OpenAP is experimental and some AirTrafficSim features such as autopilot procedural speed are not yet supported and bugs may occur.
```

To use OpenAP, set performance_mode equals to "OpenAP" instead of "BADA". The aircraft is needed similarly to [`DemoEnv`](./creating_env.md) but flight plan and airport information should not be added since they are yet to be supported. After adding the aircraft, set the speed of each aircraft using the `set_speed()` function to disable auto procedural speed. 


```{code-block} python
---
lineno-start: 9
emphasize-lines: 10, 18, 19
caption: airtrafficsim_data/environment/OpenApDemo.py
---
class OpenApDemo(Environment):

    def __init__(self):
        # Initialize environment super class
        super().__init__(file_name=Path(__file__).name.removesuffix('.py'),  # File name (do not change)
                         start_time=datetime.fromisoformat(
                             '2022-03-22T00:00:00+00:00'),
                         end_time=1000,
                         weather_mode="",
                         performance_mode="OpenAP"
                         )

        # Add aircraft
        self.aircraft_head = Aircraft(self.traffic, call_sign="HEAD", aircraft_type="A320", flight_phase=FlightPhase.CRUISE, configuration=Config.CLEAN,
                                      lat=22.019213, long=113.539164, alt=20000.0, heading=175.0, cas=250.0, fuel_weight=10000.0, payload_weight=12000.0, cruise_alt=37000)
        self.aircraft_fol = Aircraft(self.traffic, call_sign="FOLLOW", aircraft_type="A320", flight_phase=FlightPhase.CRUISE, configuration=Config.CLEAN,
                                     lat=21.9, long=113.5, alt=20000.0, heading=175.0, cas=310.0, fuel_weight=10000.0, payload_weight=12000.0, cruise_alt=37000)
        self.aircraft_head.set_speed(250.0) # To set the aircraft to follow given speed command instead of auto procedural
        self.aircraft_fol.set_speed(310.0) # To set the aircraft to follow given speed command instead of auto procedural
```