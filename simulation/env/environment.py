from utils.enums import Flight_phase
from traffic.traffic import Traffic
from traffic.aircraft import Aircraft

class Environment:

    def __init__(self):

        self.global_time = 0                    # [s]
        self.time_to_target = 0                 # [s]

        self.traffic = Traffic('simulation', 2)
        self.aircraft_head = Aircraft(self.traffic, "HEAD", "A20N", Flight_phase.CRUISE, 22.387778, 113.428116, 20000.0, 175.0, 310.0, 10000.0, 12000.0, ["SIERA", "CANTO", "MURRY", "GOODI", "SILVA", "LIMES"])
        self.aircraft_fol = Aircraft(self.traffic, "FOLLOW", "A20N", Flight_phase.CRUISE, 21.9, 113.5, 20000.0, 175.0, 310.0, 10000.0, 12000.0)
        

    def step(self):
        print("")
        print("Environment - step(), time = ", self.global_time)
        print("")
        print("Set ATC command")
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

        print("update states")
        self.traffic.update()
        print("Save to file")
        self.traffic.save(self.global_time)
        self.global_time += 1
        
