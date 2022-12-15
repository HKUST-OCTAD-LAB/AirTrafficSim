import numpy as np

from airtrafficsim.core.traffic import Traffic
from airtrafficsim.core.navigation import Nav
from airtrafficsim.utils.unit_conversion import Unit
from airtrafficsim.utils.calculation import Cal
from airtrafficsim.utils.enums import APLateralMode, APThrottleMode


class Aircraft:
    """
    Aircraft class to represent the states of one individual aircraft, including get and set functions.
    """

    def __init__(self, traffic: Traffic, call_sign, aircraft_type, flight_phase, configuration, lat, long, alt, heading, cas, fuel_weight, payload_weight, departure_airport="", departure_runway="", sid="", arrival_airport="", arrival_runway="", star="", approach="", flight_plan=[], cruise_alt=-1):
        """
        Initialize one aircraft and add the aircraft to traffic array.
        """
        self.traffic = traffic          # Pass traffic array reference
        self.index = self.traffic.add_aircraft(call_sign, aircraft_type, flight_phase, configuration, lat, long, alt, heading, cas, fuel_weight, payload_weight,
                                               departure_airport, departure_runway, sid, arrival_airport, arrival_runway, star, approach, flight_plan, cruise_alt)        # Add aircraft. Obtain aircraft index
        self.vectoring = ""

    def set_heading(self, heading):
        """Set heading [deg]"""
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.heading[index] = heading
        self.traffic.ap.lateral_mode[index] = APLateralMode.HEADING

    def set_speed(self, speed):
        """Set CAS [kt]"""
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.cas[index] = speed
        self.traffic.ap.auto_throttle_mode[index] = APThrottleMode.SPEED

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
        self.traffic.ap.lateral_mode[index] = APLateralMode.LNAV

    def set_holding(self, holding_time, holding_fix, region):
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.holding_round[index] = holding_time
        self.traffic.ap.holding_info[index] = Nav.get_holding_procedure(
            holding_fix, region)

    def set_vectoring(self, vectoring_time, v_2, fix):

        if not self.vectoring == fix and self.get_next_wp() == fix:
            self.vectoring = fix
            index = np.where(self.traffic.index == self.index)[0][0]

            new_dist = self.traffic.ap.dist[index] + Unit.kts2mps(
                self.traffic.cas[index] + v_2) * (vectoring_time) / 2000.0
            bearing = np.mod(self.traffic.ap.heading[index]+np.rad2deg(
                np.arccos(self.traffic.ap.dist[index]/new_dist)) + 360.0, 360.0)
            lat, long = Cal.cal_dest_given_dist_bearing(
                self.traffic.lat[index], self.traffic.long[index], bearing, new_dist / 2)

            # Add new virtual waypoint
            i = self.traffic.ap.flight_plan_index[index]
            self.traffic.ap.flight_plan_lat[index].insert(i, lat)
            self.traffic.ap.flight_plan_long[index].insert(i, long)
            self.traffic.ap.flight_plan_name[index].insert(i, "VECT")
            self.traffic.ap.flight_plan_target_alt[index].insert(
                i, self.traffic.ap.flight_plan_target_alt[index][i])
            self.traffic.ap.flight_plan_target_speed[index][i] = v_2
            self.traffic.ap.flight_plan_target_speed[index].insert(
                i, self.traffic.ap.flight_plan_target_speed[index][i])

    def resume_own_navigation(self):
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.ap.lateral_mode[index] = APLateralMode.LNAV
        self.traffic.ap.auto_throttle_mode[index] = APThrottleMode.AUTO

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

    def get_next_wp(self):
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.ap.flight_plan_name[index][self.traffic.ap.flight_plan_index[index]]

    def get_wake(self):
        index = np.where(self.traffic.index == self.index)[0][0]
        return self.traffic.perf.perf_model._Bada__wake_category[index]
