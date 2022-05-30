from datetime import datetime
from pathlib import Path
import numpy as np

from core.environment import Environment
from core.aircraft import Aircraft
from utils.enums import Configuration, Flight_phase

class FullFlightDemo(Environment):

    def __init__(self):
        # Initialize environment super class
        super().__init__(file_name = Path(__file__).name.removesuffix('.py'), #File name (do not change)
                        number_of_traffic = 1,
                        start_time = datetime.fromisoformat('2022-03-22T00:00:00'),
                        end_time = 10000,
                        era5_weather = False,
                        bada_perf = True 
                        )

        # Add aircraft
        self.aircraft_full = Aircraft(self.traffic, call_sign="FULL", aircraft_type="A320", flight_phase=Flight_phase.TAKEOFF, configuration=Configuration.TAKEOFF,
                                                    lat=22.307500, long=113.932833, alt=0.0, heading=254.0, cas=149.0, 
                                                    fuel_weight=5273.0, payload_weight=12000.0,
                                                    departure_airport = "VHHH", departure_runway="RW25L", sid = "OCEA2B",
                                                    arrival_airport="RCTP", arrival_runway="RW05R", star = "TONG1A", approach = "I05R",
                                                    flight_plan=["RASSE", "CONGA", "ENVAR", "DADON", "EXTRA", "RENOT"],
                                                    cruise_alt=37000)
                                                    # target_alt=[    5000,   14000,  37000,    37000,   37000,   37000,   37000,   37000,   37000,   37000,   37000,   37000,   29000,    4000,    4000,    4000])
                                                    # VHHH/25L OCEAN2B OCEAN V3 ENVAR M750 TONGA TONGA1A RCTP/05R
                                                    # departure_runway=[22.182675,113.555815], "HOKOU", "TULIP" approach
                                                    # TODO: 0 cas

    def should_end(self):
        if (self.global_time > 60 and  np.all((self.traffic.alt == 0))):
            return True
        else:
            return False
        

    def atc_command(self):
        # User algorithm
        print("Set ATC command")
        
