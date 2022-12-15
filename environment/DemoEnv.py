from datetime import datetime
from pathlib import Path

from airtrafficsim.core.environment import Environment
from airtrafficsim.core.aircraft import Aircraft
from airtrafficsim.utils.enums import Config, FlightPhase


class DemoEnv(Environment):

    def __init__(self):
        # Initialize environment super class
        super().__init__(file_name=Path(__file__).name.removesuffix('.py'),  # File name (do not change)
                         start_time=datetime.fromisoformat(
                             '2022-03-22T00:00:00+00:00'),
                         end_time=1000,
                         weather_mode="",
                         performance_mode="BADA"
                         )

        # Add aircraft
        self.aircraft_head = Aircraft(self.traffic, call_sign="HEAD", aircraft_type="A20N", flight_phase=FlightPhase.CRUISE, configuration=Config.CLEAN,
                                      lat=22.019213, long=113.539164, alt=20000.0, heading=175.0, cas=250.0, fuel_weight=10000.0, payload_weight=12000.0,
                                      arrival_airport="VHHH", arrival_runway="07R", star="SIER7A", approach="I07R", cruise_alt=37000)
        # self.aircraft_head.set_speed(250.0) # To set the aircraft to follow given speed command instead of auto procedural
        self.aircraft_fol = Aircraft(self.traffic, call_sign="FOLLOW", aircraft_type="A20N", flight_phase=FlightPhase.CRUISE, configuration=Config.CLEAN,
                                     lat=21.9, long=113.5, alt=20000.0, heading=175.0, cas=310.0, fuel_weight=10000.0, payload_weight=12000.0, cruise_alt=37000)

    def should_end(self):
        return False

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
