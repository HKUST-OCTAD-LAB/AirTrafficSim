from traffic.src.aircraft.aircraft import Aircraft

class Environment:

    def __init__(self):

        self.global_time = 0            # [s]
        self.wp_setting = []            # [[lat , long]]
        self.pos_head = []              # [[lat , long]]
        self.v_head = 250               # [knots]
        self.pos_fol = []               # [[lat , long]]
        self.v_fol = 250                # [knots]
        self.time_to_target = 0                 # [s]
        self.aircraft_type_head = ""            #[string]
        self.aircraft_type_fol = ""             #[string]

        self.wind_n = 0                 # [knots]
        self.wind_e = 0                 # [knots]

        self.aircraft_head = Aircraft(21.98667, 113.553333, 175, 300)
        self.aircraft_fol = Aircraft(21.9, 113.5, 175, 300)


    def step(self, heading, velocity = 300):
        print("Update following aircraft")  
        self.aircraft_fol.update(180)
        print("")
        print("Update heading aircraft")
        self.aircraft_head.update(173)
        print("")
