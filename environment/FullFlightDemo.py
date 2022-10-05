from datetime import datetime
from pathlib import Path

from airtrafficsim.core.environment import Environment
from airtrafficsim.core.aircraft import Aircraft
from airtrafficsim.core.navigation import Nav
from airtrafficsim.utils.enums import Config, FlightPhase

class FullFlightDemo(Environment):

    def __init__(self):
        # Initialize environment super class
        super().__init__(file_name = Path(__file__).name.removesuffix('.py'), #File name (do not change)
                        start_time = datetime.fromisoformat('2022-03-22T00:00:00'),
                        end_time = 7000,
                        weather_mode = "",
                        performance_mode = "BADA" 
                        )

        # Add aircraft
        lat_dep, long_dep, alt_dep = Nav.get_runway_coord("VHHH", "25L")
        self.aircraft_full = Aircraft(self.traffic, call_sign="FULL", aircraft_type="A320", flight_phase=FlightPhase.TAKEOFF, configuration=Config.TAKEOFF,
                                      lat=lat_dep, long=long_dep, alt=alt_dep, heading=254.0, cas=149.0,
                                      fuel_weight=5273.0, payload_weight=12000.0,
                                      departure_airport = "VHHH", departure_runway="RW25L", sid = "OCEA2B",
                                      arrival_airport="RCTP", arrival_runway="05R", star = "TONG1A", approach = "I05R",
                                      flight_plan=["RASSE", "CONGA", "ENVAR", "DADON", "EXTRA", "RENOT"],
                                      cruise_alt=37000)

    def should_end(self):
        # if (self.global_time > 60 and  np.all((self.traffic.alt == 0))):
        #     return True
        # else:
            return False
        

    def atc_command(self):
        # User algorithm
        pass
        
