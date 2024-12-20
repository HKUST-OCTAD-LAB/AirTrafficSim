from typing import Any

import numpy as np
from airtrafficsim.core.navigation import Nav
from airtrafficsim.core.traffic import Traffic
from airtrafficsim.utils.calculation import Cal
from airtrafficsim.utils.enums import (
    APLateralMode,
    APThrottleMode,
    Config,
    FlightPhase,
)
from airtrafficsim.utils.unit_conversion import Unit


class Aircraft:
    """
    Aircraft class to represent the states of one individual aircraft, including
    get and set functions.
    """

    def __init__(
        self,
        traffic: Traffic,
        call_sign: str,
        aircraft_type: str,
        flight_phase: FlightPhase,
        configuration: Config,
        lat: float,
        long: float,
        alt: float,
        heading: float,
        cas: float,
        fuel_weight: float,
        payload_weight: float,
        departure_airport: str = "",
        departure_runway: str = "",
        sid: str = "",
        arrival_airport: str = "",
        arrival_runway: str = "",
        star: str = "",
        approach: str = "",
        flight_plan: list[Any] = [],  # FIXME: check correct type
        cruise_alt: int = -1,
    ):
        """
        Initialize one aircraft and add the aircraft to traffic array.

        Parameters
        ----------
        traffic : Traffic
            Points to the traffic array class. (The value must be self.traffic)
        call_sign : str
            Call sign of the aircraft
        aircraft_type : str
            ICAO aircraft type
        flight_phase : FlightPhase.enums
            Initial flight phase
        configuration : Configuration.enums
            Initial configuration
        lat : float
            Initial latitude [deg]
        long : float
            Initial longitude [deg]
        alt : float
            Initial altitude [ft]
        heading : float
            Initial heading [deg]
        cas : float
            Initial CAS [kt]
        fuel_weight : float
            Initial fuel weight [kg]
        payload_weight : float
            Initial payload weight [kg]
        departure_airport : str, optional
            ICAO code of departure airport, by default ""
        departure_runway : str, optional
            Departure runway, by default ""
        sid : str, optional
            ICAO code of Standard Instrument Departure, by default ""
        arrival_airport : str, optional
            ICAO code of arrival airport, by default ""
        arrival_runway : str, optional
            Arrival runway, by default ""
        star : str, optional
            ICAO code Standard Terminal Arrival Procedure, by default ""
        approach : str, optional
            ILS approach procedure, by default ""
        flight_plan : list, optional
            Array of waypoints that the aircraft will fly, by default []
        cruise_alt : int, optional
            Target cruise altitude [ft], by default -1
        """
        self.traffic = traffic  # Pass traffic array reference
        self.index = self.traffic.add_aircraft(
            call_sign,
            aircraft_type,
            flight_phase,
            configuration,
            lat,
            long,
            alt,
            heading,
            cas,
            fuel_weight,
            payload_weight,
            departure_airport,
            departure_runway,
            sid,
            arrival_airport,
            arrival_runway,
            star,
            approach,
            flight_plan,
            cruise_alt,
        )  # Add aircraft. Obtain aircraft index
        self.vectoring = ""

    def set_heading(self, heading: float) -> None:
        """
        Set the heading of the aircraft.

        Parameters
        ----------
        heading : float
            Heading [deg]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.autopilot.heading[index] = heading
        self.traffic.autopilot.lateral_mode[index] = APLateralMode.HEADING

    def set_speed(self, speed: float) -> None:
        """
        Set the speed of the aircraft.

        Parameters
        ----------
        speed : float
            Speed [kt]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.autopilot.cas[index] = speed
        self.traffic.autopilot.auto_throttle_mode[index] = APThrottleMode.SPEED

    def set_vs(self, vs: float) -> None:
        """
        Set vertical speed.

        Parameters
        ----------
        vs : float
            Vertical speed [ft/min]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.autopilot.vs[index] = vs

    def set_alt(self, alt: float) -> None:
        """
        Set altitude.

        Parameters
        ----------
        alt : float
            Altitude [ft]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.autopilot.alt[index] = alt

    def set_direct(self, waypoint: str) -> None:
        """
        Set direct to a waypoint.

        Parameters
        ----------
        waypoint : str
            ICAO code of the waypoint
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.autopilot.lateral_mode[index] = APLateralMode.LNAV

    def set_holding(
        self, holding_time: float, holding_fix: str, region: str
    ) -> None:
        """
        Set holding procedure.

        Parameters
        ----------
        holding_time : float
            How long should the aircraft hold [second]
        holding_fix : str
            ICAO code of the fix that the aircraft should hold
        region : str
            ICAO code of the region that the aircraft should hold
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.autopilot.holding_round[index] = holding_time
        self.traffic.autopilot.holding_info[index] = Nav.get_holding_procedure(
            holding_fix, region
        )

    def set_vectoring(
        self, vectoring_time: float, v_2: float, fix: str
    ) -> None:
        """
        Set vectoring procedure.

        Parameters
        ----------
        vectoring_time : float
            How long should the aircraft vector [second]
        v_2 : float
            The target speed speed [kt]
        fix : str
            ICAO code of the fix that the aircraft go next after vectoring
        """
        if not self.vectoring == fix and self.get_next_wp() == fix:
            self.vectoring = fix
            index = np.where(self.traffic.index == self.index)[0][0]

            new_dist = (
                self.traffic.autopilot.dist[index]
                + Unit.kts2mps(self.traffic.cas[index] + v_2)
                * (vectoring_time)
                / 2000.0
            )
            bearing = np.mod(
                self.traffic.autopilot.heading[index]
                + np.rad2deg(
                    np.arccos(self.traffic.autopilot.dist[index] / new_dist)
                )
                + 360.0,
                360.0,
            )
            lat, long = Cal.cal_dest_given_dist_bearing(
                self.traffic.lat[index],
                self.traffic.long[index],
                bearing,
                new_dist / 2,
            )

            # Add new virtual waypoint
            i = self.traffic.autopilot.flight_plan_index[index]
            self.traffic.autopilot.flight_plan_lat[index].insert(i, lat)
            self.traffic.autopilot.flight_plan_long[index].insert(i, long)
            self.traffic.autopilot.flight_plan_name[index].insert(i, "VECT")
            self.traffic.autopilot.flight_plan_target_alt[index].insert(
                i, self.traffic.autopilot.flight_plan_target_alt[index][i]
            )
            self.traffic.autopilot.flight_plan_target_speed[index][i] = v_2
            self.traffic.autopilot.flight_plan_target_speed[index].insert(
                i, self.traffic.autopilot.flight_plan_target_speed[index][i]
            )

    def resume_own_navigation(self) -> None:
        """
        Resume own navigation to use autopilot instead of user commanded target.
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        self.traffic.autopilot.lateral_mode[index] = APLateralMode.LNAV
        self.traffic.autopilot.auto_throttle_mode[index] = APThrottleMode.AUTO

    def get_heading(self) -> float:
        """
        Get heading of aircraft.

        Returns
        -------
        Heading : float
            Heading [deg]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return float(self.traffic.heading[index])

    def get_cas(self) -> float:
        """
        Get Calibrated air speed of aircraft.

        Returns
        -------
        cas : float
            Calibrated air speed [knots]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return float(self.traffic.cas[index])

    def get_mach(self) -> float:
        """
        Get Mach number of aircraft.

        Returns
        -------
        mach : float
            Mach number [dimensionless]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return float(self.traffic.mach[index])

    def get_vs(self) -> float:
        """
        Get vertical speed of aircraft.

        Returns
        -------
        vs : float
            Vertical speed [ft/min]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return float(self.traffic.vs[index])

    def get_alt(self) -> float:
        """
        Get altitude of aircraft.

        Returns
        -------
        alt : float[]
            Altitude [ft]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return float(self.traffic.alt[index])

    def get_long(self) -> float:
        """
        Get longitude of aircraft.

        Returns
        -------
        long : float
            Longitude [deg]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return float(self.traffic.long[index])

    def get_lat(self) -> float:
        """
        Get latitude of aircraft.

        Returns
        -------
        lat : float
            Latitude [deg]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return float(self.traffic.lat[index])

    def get_fuel_consumed(self) -> float:
        """
        Get the total fuel consumed of aircraft.

        Returns
        -------
        fuel_consumed : float
            Fuel consumed [kg]
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return float(self.traffic.fuel_consumed[index])

    def get_next_wp(self) -> str:
        """
        Get next waypoint.

        Returns
        -------
        waypoint : str
            ICAO code of the next waypoing
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return str(
            self.traffic.autopilot.flight_plan_name[index][
                self.traffic.autopilot.flight_plan_index[index]
            ]
        )

    def get_wake(self) -> str:
        """
        Get wake category of aircraft.

        Returns
        -------
        Wake category : str
            The ICAO wake category of the aircraft.
        """
        index = np.where(self.traffic.index == self.index)[0][0]
        return str(
            self.traffic.perf.perf_model._Bada__wake_category[index]  # type: ignore
            # FIXME(abrah): why access private?????
        )
