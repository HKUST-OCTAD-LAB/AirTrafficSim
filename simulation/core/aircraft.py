from core.traffic import Traffic

from utils.enums import AP_lateral_mode, AP_throttle_mode

class Aircraft:
    """
    Aircraft class to represent the states of one individual aircraft, including get and set functions.
    """

    def __init__(self, traffic:Traffic, call_sign, aircraft_type, flight_phase, configuration, lat, long, alt, heading, cas, fuel_weight, payload_weight, departure_airport="", departure_runway="", sid="", arrival_airport="", arrival_runway="", star="", approach="", flight_plan=[], cruise_alt=-1):
        """
        Initialize one aircraft and add the aircraft to traffic array.
        """
        self.traffic = traffic          # Pass traffic array reference
        self.index = self.traffic.add_aircraft(call_sign, aircraft_type, flight_phase, configuration, lat, long, alt, heading, cas, fuel_weight, payload_weight, departure_airport, departure_runway, sid, arrival_airport, arrival_runway, star, approach, flight_plan, cruise_alt)        # Add aircraft. Obtain aircraft index


    def set_heading(self, heading):
        """Set heading [deg]"""
        self.traffic.ap.heading[self.index] = heading
        self.traffic.ap.lateral_mode[self.index] = AP_lateral_mode.HEADING


    def set_speed(self, speed):
        """Set CAS [kt]"""
        self.traffic.ap.cas[self.index] = speed
        self.traffic.ap.auto_throttle_mode[self.index] = AP_throttle_mode.SPEED

    
    # def set_mach(self, mach):
    #     """Set Mach [dimensionless]"""
    #     self.traffic.ap.mach[self.index] = mach


    def set_vs(self, vs):
        """Set vertical speed [ft/min]"""
        self.traffic.ap.vs[self.index] = vs


    def set_alt(self, alt):
        """Set alt [ft]"""
        self.traffic.ap.alt[self.index] = alt


    def set_direct(self, waypoint):
        self.traffic.ap.lateral_mode[self.index] = AP_lateral_mode.LNAV


    def resume_own_navigation(self):
        self.traffic.ap.lateral_mode[self.index] = AP_lateral_mode.LNAV
        self.traffic.ap.auto_throttle_mode[self.index] = AP_throttle_mode.AUTO


    def get_heading(self):
        """
        Get heading of aircraft.

        Returns
        -------
        Heading : float
            Heading [deg]
        """
        return self.traffic.heading[self.index]

    def get_cas(self):
        """
        Get Calibrated air speed of aircraft.

        Returns
        -------
        cas : float
            Calibrated air speed [knots]
        """
        return self.traffic.cas[self.index]

    def get_mach(self):
        """
        Get Mach number of aircraft.

        Returns
        -------
        mach : float
            Mach number [dimensionless]
        """
        return self.traffic.mach[self.index]

    def get_vs(self):
        """
        Get vertical speed of aircraft.

        Returns
        -------
        vs : float
            Vertical speed [ft/min]
        """
        return self.traffic.vs[self.index]

    def get_alt(self):
        """
        Get altitude of aircraft.

        Returns
        -------
        alt : float[]
            Altitude [ft]
        """
        return self.traffic.alt[self.index]

    def get_long(self):
        """
        Get longitude of aircraft.

        Returns
        -------
        long : float
            Longitude [deg]
        """
        return self.traffic.long[self.index]

    def get_lat(self):
        """
        Get latitude of aircraft.

        Returns
        -------
        lat : float
            Latitude [deg]
        """
        return self.traffic.lat[self.index]

    
    def get_fuel_consumed(self):
        """
        Get the total fuel consumed of aircraft.

        Returns
        -------
        fuel_consumed : float
            Fuel consumed [kg]
        """
        return self.traffic.fuel_consumed[self.index]



    
