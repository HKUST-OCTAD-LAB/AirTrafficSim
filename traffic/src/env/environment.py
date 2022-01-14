

class Environment:

    def __init__(self) -> None:

        self.global_time = 0            # [s]
        self.wp_setting = []            # [[long, lat]]
        self.pos_head = []              # [long, lat]
        self.v_head = 250               # [knots]
        self.pos_fol = []               # [long, lat]
        self.v_fol = 250                # [knots]
        self.time_to_target = 0                 # [s]
        self.aircraft_type_head = ""            #[string]
        self.aircraft_type_fol = ""             #[string]


    

    pass