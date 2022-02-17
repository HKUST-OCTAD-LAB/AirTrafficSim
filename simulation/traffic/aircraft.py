from traffic.traffic import Traffic

class Aircraft:

    def __init__(self, traffic:Traffic, call_sign, aircraft_type, flight_phase, lat, long, alt, heading, tas, weight, fuel_weight, payload_weight):
        """
        Initialize one aircraft.

        Parameters
        ----------
        
        """
        self.traffic = traffic          # Pass traffic array reference
        self.index = traffic.add_aircraft(call_sign, aircraft_type, flight_phase, lat, long, alt, heading, tas, weight, fuel_weight, payload_weight)        # Add aircraft. Obtain aircraft index


    def set_heading(self, heading):
        "Set heading [deg]"
        self.traffic.ap.heading[self.index] = heading

    def set_speed(self, speed):
        """Set CAS [kt]"""
        self.traffic.ap.cas[self.index] = speed

    def set_vs(self, vs):
        """Set vs [ft/min]"""
        self.traffic.ap.vs[self.index] = vs

    def set_alt(self, alt):
        pass

    def set_direct(self, waypoint):
        pass

    def resume_own_navigation(self):
        pass




    
