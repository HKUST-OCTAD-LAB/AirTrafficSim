from datetime import datetime
from pathlib import Path

from env.environment import Environment
from traffic.aircraft import Aircraft
from utils.enums import Flight_phase

class DemoEnv(Environment):

    def __init__(self):
        number_of_traffic = 2

        super().__init__(N=number_of_traffic, file_name=Path(__file__).name.removesuffix('.py'))

        # User environment setup
        self.start_time = datetime.fromisoformat('2022-03-22T00:00:00')
        self.end_time = 5000

        self.aircraft_head = Aircraft(self.traffic, "HEAD", "A20N", Flight_phase.CRUISE, 22.387778, 113.428116, 20000.0, 175.0, 310.0, 10000.0, 12000.0, ["SIERA", "CANTO", "MURRY", "GOODI", "SILVA", "LIMES"])
        self.aircraft_fol = Aircraft(self.traffic, "FOLLOW", "A20N", Flight_phase.CRUISE, 21.9, 113.5, 20000.0, 175.0, 310.0, 10000.0, 12000.0)


    def atc_command(self):
        # print("Set ATC command")
        if self.global_time == 10:  
            # Right
            self.aircraft_fol.set_heading(220)
            # Left
            # self.aircraft_head.set_heading(150)

        if self.global_time == 100:
            # Climb
            self.aircraft_fol.set_alt(10000)
            # Descend
            self.aircraft_head.set_alt(30000)

        if self.global_time == 300:
            # Accelerate
            self.aircraft_fol.set_speed(200)
            # self.aircraft_head.set_mach(0.7)
