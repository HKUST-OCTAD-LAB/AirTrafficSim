from .traffic import Traffic

class Aircraft:

    def __init__(self, traffic:Traffic, call_sign, aircraft_type, flight_phase, lat, long, alt, heading, tas, weight, fuel_weight, payload_weight):
        """
        Initialize one aircraft.

        Parameters
        ----------
        
        """
        self.traffic = traffic          # Pass traffic array reference
        self.index = traffic.add_aircraft(call_sign, aircraft_type, flight_phase, lat, long, alt, heading, tas, weight, fuel_weight, payload_weight)        # Add aircraft. Obtain aircraft index


    def __convert_tas_to_mps(tas):
        # Convert True air speed to meter per second (1nm = 1852m, 1 hr = 3600s)
        return tas * 1852 / 3600

    def set_ap_heading(self, ap_heading):
        """Temporary function"""
        
        print("aircraft.py - set_ap_heading()", ap_heading)

        self.traffic.ap_heading[self.index] = ap_heading

    def update(self):
        """
        Update an aircraft state for each timestep.
        """

        print("aircraft.py - update()")
        
        self.traffic.update(self.index)


    
