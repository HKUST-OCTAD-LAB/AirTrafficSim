import csv
from pathlib import Path
from utils.enums import Flight_phase
from traffic.traffic import Traffic
from traffic.aircraft import Aircraft

class Environment:

    def __init__(self):

        self.global_time = 0                    # [s]
        self.time_to_target = 0                 # [s]

        self.traffic = Traffic(2)
        self.aircraft_head = Aircraft(self.traffic, "HEAD", "A20N", Flight_phase.CRUISE, 21.98667, 113.553333, 20000.0, 175.0, 310.0, 5000.0, 0.0)
        self.aircraft_fol = Aircraft(self.traffic, "FOLLOW", "A20N", Flight_phase.CRUISE, 21.9, 113.5, 20000.0, 175.0, 310.0, 5000.0, 0.0)
        
        self.writer = csv.writer(open(Path(__file__).parent.parent.parent.resolve().joinpath('./server/data/simulation/simulation.csv'), 'w+'))
        header = ['time', 'id', 'callsign', 'lat', 'long', 'alt', 'heading', 'cas', 'tas', 'mach', 'vs', 'weight', 'fuel_consumed',
                    'bank_angle', 'trans_alt', 'accel', 'drag', 'esf', 'thrust', 'flight_phase', 'speed_mode', 'ap_speed_mode'] #debug
        self.writer.writerow(header)


    def step(self):
        print("")
        print("Environment - step(), time = ", self.global_time)
        print("")
        print("Set ATC command")
        if self.global_time == 10:  
            # Right
            self.aircraft_fol.set_heading(220)
            # Left
            self.aircraft_head.set_heading(150)

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
        self.traffic.save(self.writer, self.global_time)
        self.global_time += 1
        
