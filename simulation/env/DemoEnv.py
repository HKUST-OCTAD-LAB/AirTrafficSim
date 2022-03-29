from datetime import datetime
from pathlib import Path

from env.environment import Environment
from traffic.aircraft import Aircraft
from utils.enums import Flight_phase

class DemoEnv(Environment):

    def __init__(self):
        # User setting
        number_of_traffic = 2

        # Initialize environment super class (Do not change)
        super().__init__(N=number_of_traffic, file_name=Path(__file__).name.removesuffix('.py'))

        # User setting
        self.start_time = datetime.fromisoformat('2022-03-22T00:00:00')
        self.end_time = 1500
        self.aircraft_head = Aircraft(self.traffic, call_sign="HEAD", aircraft_type="A20N", flight_phase=Flight_phase.CRUISE, 
                                                    lat=22.387778, long=113.428116, alt=20000.0, heading=175.0, cas=250.0, fuel_weight=10000.0, payload_weight=12000.0, 
                                                    flight_plan=["SIERA", "CANTO", "MURRY", "SILVA", "LIMES"])
        self.aircraft_fol = Aircraft(self.traffic, call_sign="FOLLOW", aircraft_type="A20N", flight_phase=Flight_phase.CRUISE, 
                                                    lat=21.9, long=113.5, alt=20000.0, heading=175.0, cas=310.0, fuel_weight=10000.0, payload_weight=12000.0)


    def atc_command(self):
        # User algorithm
        print("Set ATC command")
        if self.global_time == 10:  
            # Right
            self.aircraft_fol.set_heading(220)
            # Left
            # self.aircraft_head.set_heading(150)

        if self.global_time == 100:
            # Accelerate
            # self.aircraft_fol.set_mach(0.7)
            self.aircraft_head.set_speed(250)

        if self.global_time == 300:
            # Climb
            self.aircraft_fol.set_alt(30000)
            # Descend
            self.aircraft_head.set_alt(11000)
