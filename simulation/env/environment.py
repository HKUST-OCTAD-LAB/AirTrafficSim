import csv
from pathlib import Path
from utils.enums import Flight_phase
from traffic.traffic import Traffic
from traffic.aircraft import Aircraft

class Environment:

    def __init__(self):

        self.global_time = 0                    # [s]
        self.wp_setting = []                    # [[lat , long]]
        self.pos_head = []                      # [[lat , long]]
        self.v_head = 250                       # [knots]
        self.pos_fol = []                       # [[lat , long]]
        self.v_fol = 250                        # [knots]
        self.time_to_target = 0                 # [s]
        self.aircraft_type_head = ""            #[string]
        self.aircraft_type_fol = ""             #[string]

        self.wind_n = 0                         # [knots]
        self.wind_e = 0                         # [knots]

        self.traffic = Traffic(2)
        self.aircraft_head = Aircraft(self.traffic, "HEAD", "A20N", Flight_phase.CRUISE, 21.98667, 113.553333, 20000.0, 175.0, 310.0, 68000.0, 5000.0, 0.0)
        self.aircraft_fol = Aircraft(self.traffic, "FOLLOW", "A20N", Flight_phase.CRUISE, 21.9, 113.5, 20000.0, 175.0, 310.0, 68000.0, 5000.0, 0.0)
        
        self.writer = csv.writer(open(Path(__file__).parent.parent.parent.resolve().joinpath('./server/data/simulation/simulation.csv'), 'w+'))
        header = ['time', 'id', 'callsign', 'lat', 'long', 'alt', 'heading', 'cas']
        self.writer.writerow(header)


    def step(self):
        print("")
        print("Environment - step(), time = ", self.global_time)
        print("")
        print("Set ATC command")  
        self.aircraft_fol.set_heading(180)
        self.aircraft_head.set_heading(170)
        print("update states")
        self.traffic.update()
        print("Save to file")
        self.traffic.save(self.writer, self.global_time)
        self.global_time += 1
        
