from core.traffic import Traffic
import numpy as np

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
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.heading[index] = heading
        self.traffic.ap.lateral_mode[index] = AP_lateral_mode.HEADING


    def set_speed(self, speed):
        """Set CAS [kt]"""
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.cas[index] = speed
        self.traffic.ap.auto_throttle_mode[index] = AP_throttle_mode.SPEED

    
    # def set_mach(self, mach):
    #     """Set Mach [dimensionless]"""
    #     self.traffic.ap.mach[self.index] = mach


    def set_vs(self, vs):
        """Set vertical speed [ft/min]"""
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.vs[index] = vs


    def set_alt(self, alt):
        """Set alt [ft]"""
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.alt[index] = alt


    def set_direct(self, waypoint):
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.lateral_mode[index] = AP_lateral_mode.LNAV


    def resume_own_navigation(self):
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.lateral_mode[index] = AP_lateral_mode.LNAV
        self.traffic.ap.auto_throttle_mode[index] = AP_throttle_mode.AUTO


    def get_heading(self):
        """
        Get heading of aircraft.

        Returns
        -------
        Heading : float
            Heading [deg]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.heading[index]

    def get_cas(self):
        """
        Get Calibrated air speed of aircraft.

        Returns
        -------
        cas : float
            Calibrated air speed [knots]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.cas[index]

    def get_mach(self):
        """
        Get Mach number of aircraft.

        Returns
        -------
        mach : float
            Mach number [dimensionless]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.mach[index]

    def get_vs(self):
        """
        Get vertical speed of aircraft.

        Returns
        -------
        vs : float
            Vertical speed [ft/min]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.vs[index]

    def get_alt(self):
        """
        Get altitude of aircraft.

        Returns
        -------
        alt : float[]
            Altitude [ft]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.alt[index]

    def get_long(self):
        """
        Get longitude of aircraft.

        Returns
        -------
        long : float
            Longitude [deg]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.long[index]

    def get_lat(self):
        """
        Get latitude of aircraft.

        Returns
        -------
        lat : float
            Latitude [deg]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.lat[index]

    
    def get_fuel_consumed(self):
        """
        Get the total fuel consumed of aircraft.

        Returns
        -------
        fuel_consumed : float
            Fuel consumed [kg]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.fuel_consumed[index]
