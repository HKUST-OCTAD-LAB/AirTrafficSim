from datetime import datetime
from pathlib import Path

from core.environment import Environment
from core.aircraft import Aircraft
from utils.enums import Configuration, Flight_phase

class DemoEnv(Environment):

    def __init__(self):
        # Initialize environment super class
        super().__init__(file_name = Path(__file__).name.removesuffix('.py'), #File name (do not change)
                        number_of_traffic = 2,
                        start_time = datetime.fromisoformat('2022-03-22T00:00:00'),
                        end_time = 1000,
                        weather_mode = "ERA%",
                        performance_mode= "Bada"
                        )

        # Add aircraft
        self.aircraft_head = Aircraft(self.traffic, call_sign="HEAD", aircraft_type="A20N", flight_phase=Flight_phase.CRUISE, configuration=Configuration.CLEAN,
                                                    lat=22.387778, long=113.428116, alt=20000.0, heading=175.0, cas=250.0, fuel_weight=10000.0, payload_weight=12000.0, 
                                                    flight_plan=["SIERA", "CANTO", "MURRY", "SILVA", "LIMES"])
        self.aircraft_fol = Aircraft(self.traffic, call_sign="FOLLOW", aircraft_type="A20N", flight_phase=Flight_phase.CRUISE, configuration=Configuration.CLEAN,
                                                    lat=21.9, long=113.5, alt=20000.0, heading=175.0, cas=310.0, fuel_weight=10000.0, payload_weight=12000.0)


    def should_end(self):
        return False

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
