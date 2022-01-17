from ..traffic import Traffic
from ..traffic import Aircraft

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

        # self.performance = Performance()
        self.traffic = Traffic()
        self.aircraft_head = Aircraft(self.traffic, "1", "A320", 3, 21.98667, 113.553333, 200, 175, 300, 0, 0, 0)
        self.aircraft_fol = Aircraft(self.traffic, "2", "A320", 3, 21.9, 113.5, 200, 175, 300, 0, 0, 0)


    def step(self):
        print("")
        print("Environment - step(), time = ", self.global_time)
        print("")
        print("Update following aircraft")  
        self.aircraft_fol.set_ap_heading(180)
        self.aircraft_fol.update()
        print("")
        print("Update heading aircraft")
        self.aircraft_head.set_ap_heading(173)
        self.aircraft_head.update()
        print("")
        self.global_time += 1
