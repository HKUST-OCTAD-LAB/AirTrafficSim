"""Performance base class"""
# FIXME(abrah): move entire thing to __init__.py

from typing import TYPE_CHECKING, Any, Literal

# FIXME(abrah): openap should be optional.
from openap import WRAP, Drag, FuelFlow, Thrust, prop
from typing_extensions import deprecated

import numpy as np

from ...types import ArrayOrFloat, array, uint_array
from ...utils.enums import APSpeedMode, Config, VerticalMode
from ...utils.unit_conversion import Unit
from .bada import Bada, MassClass

if TYPE_CHECKING:
    from ..traffic import Traffic

PerformanceMode = Literal["BADA", "OpenAP"]

_REPLACEMENT = "[airtrafficsim.experimental.performance.bada3][]"


class Performance:
    # FIXME(abrah): don't mix BADA and OpenAP.
    def __init__(self, performance_mode: PerformanceMode) -> None:
        self.performance_mode = performance_mode
        """Whether BADA performance model is used [string]"""

        if self.performance_mode == "BADA":
            self.perf_model = Bada()
        else:
            # OpenAP
            self.prop_model: list[dict[str, Any]] = []
            self.thrust_model: list[Thrust] = []
            self.drag_model: list[Drag] = []
            self.fuel_flow_model: list[FuelFlow] = []
            self.wrap_model: list[WRAP] = []

        # FIXME(abrah): why are we storing state here?
        self.drag = np.zeros([0])
        """Drag [N]"""
        self.thrust = np.zeros([0])
        """Thrust [N]"""
        self.esf = np.zeros([0])
        """Energy share factor [dimensionless]"""

        ## Atmosphere model (Ref: BADA user menu section 3.1)
        # MSL Standard atmosphere condition
        self.__T_0 = 288.15
        """Standard atmospheric temperature at MSL [K]"""
        self.__P_0 = 101325
        """Standard atmospheric pressure at MSL [Pa]"""
        self.__RHO_0 = 1.225
        """Standard atmospheric density at MSL [kg/m^3]"""
        self.__A_0 = 340.294
        """Speed of sound [m/s]"""
        # Expression
        self.__KAPPA = 1.4
        """Adiabatic index of air [dimensionless]"""
        self.__R = 287.05287
        """Real gas constant of air [m^2/(K*s^2)]"""
        self.__G_0 = 9.80665
        """Gravitational acceleration [m/s^2]"""
        self.__BETA_T_BELOW_TROP = -0.0065
        """ISA temperature gradient with altitude below the tropopause [K/m]"""
        # Tropopause (separation between troposphere (below)
        # and stratosphere (above))
        self.__H_P_TROP = 11000
        """Geopotential pressure altitude [m]"""

    # FIXME(abrah): mass class should be enum
    def add_aircraft(
        self, icao: str, mass_class: MassClass = MassClass.AV
    ) -> None:
        """
        Add an aircraft to traffic array.

        Returns
        -------
        n: int
            Index of the added aircraft
        """
        self.drag = np.append(self.drag, 0.0)
        self.thrust = np.append(self.thrust, 0.0)
        self.esf = np.append(self.esf, 0.0)

        if self.performance_mode == "BADA":
            self.perf_model.add_aircraft(icao, mass_class)
        else:
            self.prop_model.append(prop.aircraft(icao))
            self.thrust_model.append(
                Thrust(ac=icao, eng=prop.aircraft_engine_options(icao)[0])
            )
            self.drag_model.append(Drag(ac=icao))
            self.fuel_flow_model.append(
                FuelFlow(ac=icao, eng=prop.aircraft_engine_options(icao)[0])
            )
            self.wrap_model.append(WRAP(ac=icao))

    def del_aircraft(self, index: int) -> None:
        """
        Delete an aircraft from traffic array.
        """
        self.drag = np.delete(self.drag, index)
        self.thrust = np.delete(self.thrust, index)
        self.esf = np.delete(self.esf, index)
        if self.performance_mode == "BADA":
            self.perf_model.del_aircraft(index)
        else:
            del self.prop_model[index]
            del self.thrust_model[index]
            del self.drag_model[index]
            del self.fuel_flow_model[index]
            del self.wrap_model[index]

    def init_procedure_speed(self, mass: array, n: int) -> None:
        """
        Initialize standard air speed schedule for all flight phases
        (Section 4.1-4.3)

        Parameters
        ----------
        mass: float[]
            Aircraft mass [kg]

        n: int
            Index of performance array.
        """
        if self.performance_mode == "BADA":
            self.perf_model.init_procedure_speed(mass, n)

    def get_procedure_speed(
        self, H_p: array, H_p_trans: array, flight_phase: uint_array
    ) -> array:
        """
        Get the standard air speed schedule

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [ft]

        H_p_trans: float[]
            Transition altitude [ft]

        flight_phase: float[]
            Flight phase from Traffic class [Flight_phase enum]

        Returns
        -------
        v_std: float[]
            Standard CAS [kt]
        -or-
        M_std: float[]
            Standard Mach [dimensionless]
        """
        # FIXME(abrah): dont return v or M!!!
        if self.performance_mode == "BADA":
            return self.perf_model.get_procedure_speed(
                H_p, H_p_trans, flight_phase
            )
        else:
            return np.where(H_p > 0, 20000, 20000)

    ### Atmosphere model (Ref: BADA user menu section 3.1)

    @deprecated(_REPLACEMENT)
    def cal_temperature(self, H_p: array | float, d_T: array | float) -> array:
        """
        Calculate Temperature (Equation 3.1-12~16)

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [m]

        d_T: float[]
            Temperature differential at MSL [K]

        Returns
        -------
        T_< if below tropopause: float[]
            Temperature [K]

        T_trop or T_> if equal to or above tropopause: float[]
            Temperature [K]
        """
        return np.where(
            H_p < self.__H_P_TROP,
            # If below Geopotential pressure altitude of tropopause
            self.__T_0 + d_T + self.__BETA_T_BELOW_TROP * H_p,
            # If equal or above Geopotential pressure altitude of tropopause
            self.__T_0 + d_T + self.__BETA_T_BELOW_TROP * self.__H_P_TROP,
        )

    @deprecated(_REPLACEMENT)
    def cal_air_pressure(
        self, H_p: array | float, T: array, d_T: array
    ) -> array:
        r"""
        Calculate Air Pressure (Equation 3.1-17~20)

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [m]

        T: float[]
            Temperature from cal_temperature()[K]

        d_T: float[]
            Temperature differential at MSL [K]

        Returns
        -------
        p_< or p_trop if below or equal to tropopause: float[]
            Pressure [Pa]

        p_> if above tropopause: float[]
            Pressure [Pa]
        """
        return np.where(
            H_p <= self.__H_P_TROP,
            # If below or equal Geopotential pressure altitude of tropopause
            # (Equation 3.1-18)
            self.__P_0
            * np.power(
                (T - d_T) / self.__T_0,
                -self.__G_0 / (self.__BETA_T_BELOW_TROP * self.__R),
            ),
            # If above Geopotential pressure altitude of tropopause
            # (Equation 3.1-20)
            self.__P_0
            * np.power(
                (self.cal_temperature(self.__H_P_TROP, d_T) - d_T) / self.__T_0,
                -self.__G_0 / (self.__BETA_T_BELOW_TROP * self.__R),
            )
            * np.exp(
                -self.__G_0
                / (self.__R * self.cal_temperature(self.__H_P_TROP, 0.0))
                * (H_p - self.__H_P_TROP)
            ),
        )

    @deprecated(_REPLACEMENT)
    def cal_air_density(self, p: ArrayOrFloat, T: ArrayOrFloat) -> ArrayOrFloat:
        """
        Calculate Air Density (Equation 3.1-21)

        Parameters
        ----------
        p: float[]
            Pressure [Pa]

        T: float[]
            Temperature [K]

        Returns
        -------
        rho: float[]
            Density [kg/m^3]
        """
        return p / (self.__R * T)

    @deprecated(_REPLACEMENT)
    def cal_speed_of_sound(self, T: ArrayOrFloat) -> ArrayOrFloat:
        """
        Calculate speed of sound. (Equation 3.1-22)

        Parameters
        ----------
        T: float[]
            Temperature [K]

        Returns
        -------
        a: float[]
            Speed of sound [m/s]
        """
        return (self.__KAPPA * self.__R * T) ** 0.5  # type: ignore

    @deprecated(_REPLACEMENT)
    def cas_to_tas(
        self, V_cas: ArrayOrFloat, p: ArrayOrFloat, rho: ArrayOrFloat
    ) -> ArrayOrFloat:
        """
        Convert Calibrated air speed to True air speed. (Equation 3.1-23)

        Parameters
        ----------
        V_cas: float[]
            Calibrated air speed [m/s]

        p: float[]
            Pressure [Pa]

        rho: float[]
            Density [kg/m^3]

        Returns
        -------
        V_tas : float[]
            True air speed [m/s]
        """
        mu = (self.__KAPPA - 1) / self.__KAPPA
        V_tas = (
            (2.0 / mu * p / rho)
            * (
                (
                    1.0
                    + self.__P_0
                    / p
                    * (
                        (
                            1.0
                            + mu
                            / 2.0
                            * self.__RHO_0
                            / self.__P_0
                            * np.square(V_cas)
                        )
                        ** (1.0 / mu)
                        - 1
                    )
                )
                ** mu
                - 1
            )
        ) ** 0.5
        return V_tas  # type: ignore

    @deprecated(_REPLACEMENT)
    def tas_to_cas(self, V_tas: array, p: array, rho: array) -> array:
        """
        Convert True air speed to Calibrated air speed. (Equation 3.1-24)

        Parameters
        ----------
        V_tas: float[]
            True air speed [m/s]

        p: float[]
            Pressure [Pa]

        rho: float[]
            Density [kg/m^3]

        Returns
        -------
        V_cas : float[]
            Calibrated air speed [m/s]
        """
        mu = (self.__KAPPA - 1) / self.__KAPPA
        V_cas = np.power(
            2
            / mu
            * self.__P_0
            / self.__RHO_0
            * (
                np.power(
                    1.0
                    + p
                    / self.__P_0
                    * (
                        np.power(
                            1 + mu / 2 * rho / p * np.square(V_tas), 1.0 / mu
                        )
                        - 1.0
                    ),
                    mu,
                )
                - 1.0
            ),
            0.5,
        )
        return V_cas  # type: ignore

    @deprecated(_REPLACEMENT)
    def mach_to_tas(self, M: array, T: array) -> array:
        """
        Convert Mach number to True Air speed (Equation 3.1-26)

        Parameters
        ----------
        M: float[]
            Mach number [dimensionless]

        T: float[]
            Temperature [K]

        Returns
        -------
        V_tas: float[]
            True air speed [m/s]
        """
        return M * np.sqrt(self.__KAPPA * self.__R * T)  # type: ignore

    @deprecated(_REPLACEMENT)
    def tas_to_mach(self, V_tas: ArrayOrFloat, T: ArrayOrFloat) -> ArrayOrFloat:
        """
        Convert True Air speed to Mach number (Equation 3.1-26)

        Parameters
        ----------
        V_tas: float[]
            True air speed [m/s]

        T: float[]
            Temperature [K]

        Returns
        -------
        M: float[]
            Mach number [dimensionless]
        """
        return V_tas / (self.__KAPPA * self.__R * T) ** 0.5  # type: ignore

    ### Operation limit
    def cal_transition_alt(self, n: int, d_T: array) -> array:
        """
        Calculate Mach/CAS transition altitude. (Equation 3.1-27~28)

        Parameters
        ----------
        d_T: float[]
            Temperature differential at MSL [K]

        Returns
        -------
        H_p_trans: float[]
            Transition altitude [m]

        Note
        ----
        Transition altitude is defined to be the geopotential pressure altitude
        at which V_CAS and M represent the same TAS value.
        """
        # TODO: Separate climb and descent trans altitude?
        if self.performance_mode == "BADA":
            V_cas = Unit.kts2mps(self.perf_model.climb_schedule[n, -2])
            M = self.perf_model.climb_schedule[n, -1]

            p_trans = (
                self.__P_0
                * (
                    np.power(
                        1.0
                        + (self.__KAPPA - 1.0)
                        / 2.0
                        * np.square(V_cas / self.__A_0),
                        self.__KAPPA / (self.__KAPPA - 1.0),
                    )
                    - 1.0
                )
                / (
                    np.power(
                        1.0 + (self.__KAPPA - 1.0) / 2.0 * np.square(M),
                        self.__KAPPA / (self.__KAPPA - 1.0),
                    )
                    - 1.0
                )
            )  # Equation 3.1-28
            p_trop = self.cal_air_pressure(
                self.__H_P_TROP, self.cal_temperature(self.__H_P_TROP, d_T), d_T
            )

            return np.where(
                p_trans >= p_trop,
                # If __p_trans >= __p_trop
                self.__T_0
                / self.__BETA_T_BELOW_TROP
                * (
                    np.power(
                        p_trans / self.__P_0,
                        -self.__BETA_T_BELOW_TROP * self.__R / self.__G_0,
                    )
                    - 1.0
                ),
                # __p_trans < __p_trop
                self.__H_P_TROP
                - self.__R
                * self.cal_temperature(self.__H_P_TROP, 0.0)
                / self.__G_0
                * np.log(p_trans / p_trop),
            )

        else:
            wrap = self.wrap_model[n]
            if not isinstance(wrap, WRAP):
                raise RuntimeError("panic: wrap_model is not WRAP")
            return wrap.climb_cross_alt_conmach()["default"] * 1000.0  # type: ignore

    def get_empty_weight(self, n: int) -> float:
        """
        Get Empty Weight of an aircraft

        Parameters
        ----------
        n: int
            index of aircraft

        Returns
        -------
        Weight: float
            Empty weight(BADA) or Operating empty weight(OpenAP) [kg]
        """
        if self.performance_mode == "BADA":
            return self.perf_model.m_min[n] * 1000.0  # type: ignore
        else:
            return self.prop_model[n]["limits"]["OEW"]  # type: ignore

    def cal_maximum_alt(self, d_T: array, m: array) -> array:
        """
        Calculate maximum altitude

        Parameters
        ----------
        d_T: float[]
            Temperature differential from ISA [K]

        m: float[]
            Aircraft mass [kg]

        Returns
        -------
        h_max: float[]
            Maximum altitude for any given mass [ft]
        """
        if self.performance_mode == "BADA":
            return self.perf_model.cal_maximum_altitude(d_T, m)
        else:
            return Unit.m2ft(
                np.array([x["limits"]["ceiling"] for x in self.prop_model])
            )

    def cal_maximum_speed(self) -> tuple[array, array]:
        """
        Calculate maximum altitude

        Returns
        -------
        speed, mach: float[]
            Maximum speed and mach
        """
        if self.performance_mode == "BADA":
            return self.perf_model.v_mo, self.perf_model.m_mo
        else:
            return np.full(len(self.prop_model), 1000), np.full(
                len(self.prop_model), 1000
            )

    def cal_minimum_speed(self, configuration: uint_array) -> array:
        """
        Calculate minimum speed

        Parameters
        ----------
        configuration: float[]
            configuration from Traffic class [configuration enum]

        Returns
        -------
        v_min: float[]
            Minimum at speed at specific configuration [knots]
        """
        if self.performance_mode == "BADA":
            return self.perf_model.cal_minimum_speed(configuration)
        else:
            # NOTE(abrah): should be resolved when we split the two
            raise RuntimeError("panic: OpenAP has no minimum/stall speed")

    def cal_max_d_tas(self, d_t: array) -> array:
        """
        Calculate maximum delta true air speed

        Parameters
        ----------
        d_t: float[]
            Timestep [s]

        Returns
        -------
        d_v: float[]
            Max delta velocity for time step [ft/s^2]
        """
        if self.performance_mode == "BADA":
            return self.perf_model.cal_max_d_tas(d_t)
        else:
            return 2 * d_t

    def cal_max_d_rocd(self, d_t: array, V_tas: array, rocd: array) -> array:
        """
        Calculate maximum delta rate of climb or descend (equation 5.2-2)

        Parameters
        ----------
        d_t: float[]
            Timestep [s]

        V_tas: float[]
            True air speed [ft/s]

        rocd: float[]
            Current rate of climb/descend [ft/s]

        Returns
        -------
        d_rocd: float[]
            Delta rate of climb or descent [ft/s^2]
        """
        if self.performance_mode == "BADA":
            return self.perf_model.cal_max_d_rocd(d_t, V_tas, rocd)
        else:
            d_rocd = np.sin(np.arcsin(rocd / V_tas) - 5.0 * d_t / V_tas) * (
                V_tas + d_t
            )
            return d_rocd  # type: ignore

    ## Performance
    ### Total Energy Model (3.2)

    def cal_energy_share_factor(
        self,
        H_p: array,
        T: array,
        d_T: array,
        M: array,
        ap_speed_mode: uint_array,
        vertical_mode: uint_array,
    ) -> array:
        """
        Calculate energy share factor (Equation 3.2-5, 8~11)

        Parameters
        ----------
        H_p: float[]
            Geopotential pressuer altitude [m]

        T: float[]
            Temperature [K]

        d_T: float[]
            Temperature differential at MSL [K]

        M: float[]
            Mach number [dimensionless]

        ap_speed_mode: float[]
            Speed mode from Autopilot class [AP_speed_mode enum]

        vertical_mode: float[]
            Vertical mode from Traffic class [Vertical_mode enum]

        Returns
        -------
        f{M}: float[]
            Energy share factor [dimenesionless]
        """
        return np.select(
            condlist=[
                ap_speed_mode == APSpeedMode.CONSTANT_MACH,
                ap_speed_mode == APSpeedMode.CONSTANT_CAS,
                ap_speed_mode == APSpeedMode.ACCELERATE,
                ap_speed_mode == APSpeedMode.DECELERATE,
            ],
            choicelist=[
                # Constant Mach
                np.where(
                    H_p > self.__H_P_TROP,
                    # Condition a: Constant Mach number in stratosphere
                    # (Equation 3.2-8)
                    1.0,
                    # Condition b: Constant Mach number below tropopause
                    # (Equation 3.2-9)
                    np.power(
                        1.0
                        + self.__KAPPA
                        * self.__R
                        * self.__BETA_T_BELOW_TROP
                        / 2.0
                        / self.__G_0
                        * np.square(M)
                        * (T - d_T)
                        / T,
                        -1.0,
                    ),
                ),
                # Constnt CAS
                np.where(
                    H_p <= self.__H_P_TROP,
                    # Condition c: Constant Calibrated Airspeed (CAS) below
                    # tropopause (Equation 3.2-10)
                    np.power(
                        1.0
                        + self.__KAPPA
                        * self.__R
                        * self.__BETA_T_BELOW_TROP
                        / 2.0
                        / self.__G_0
                        * np.square(M)
                        * (T - d_T)
                        / T
                        + np.power(
                            1.0 + (self.__KAPPA - 1.0) / 2.0 * np.square(M),
                            -1.0 / (self.__KAPPA - 1.0),
                        )
                        * (
                            np.power(
                                1.0 + (self.__KAPPA - 1.0) / 2.0 * np.square(M),
                                self.__KAPPA / (self.__KAPPA - 1.0),
                            )
                            - 1.0
                        ),
                        -1.0,
                    ),
                    # Condition d: Constant Calibrated Airspeed (CAS) above
                    # tropopause (Equation 3.2-11)
                    np.power(
                        1.0
                        + np.power(
                            1.0 + (self.__KAPPA - 1.0) / 2.0 * np.square(M),
                            -1.0 / (self.__KAPPA - 1),
                        )
                        * (
                            np.power(
                                1.0 + (self.__KAPPA - 1.0) / 2.0 * np.square(M),
                                self.__KAPPA / (self.__KAPPA - 1.0),
                            )
                            - 1.0
                        ),
                        -1.0,
                    ),
                ),
                # Acceleration in climb + Acceleration in descent
                (vertical_mode == VerticalMode.CLIMB) * 0.3
                + (vertical_mode == VerticalMode.DESCENT) * 1.7,
                # Deceleration in descent + Deceleration in climb
                (vertical_mode == VerticalMode.DESCENT) * 0.3
                + (vertical_mode == VerticalMode.CLIMB) * 1.7,
            ],
        )

    def cal_tem_rocd(
        self,
        T: array,
        d_T: array,
        m: array,
        D: array,
        f_M: array,
        Thr: array,
        V_tas: array,
        C_pow_red: array,
    ) -> array:
        """
        Total Energy Model. Speed and Throttle Controller.
        (BADA User Menu Equation 3.2-1a and 3.2-7)
        Calculate Rate of climb or descent given velocity(constant) and thrust
        (max climb thrust/idle descent).

        Parameters
        ----------
        T: float[]
            Temperature [K]

        d_T: float[]
            Temperature differential at MSL [K]

        m: float[]
            Aircraft mass [kg]

        D: float[]
            Aerodynamic drag [N]

        f_M: float[]
            Energy share factor [dimenesionless]

        Thr: float[]
            Thrust acting parallel to the aircraft velocity vector [N]

        V_tas: float[]
            True airspeed [m/s]

        C_pow_red: float[]
            Reduced climb power coefficient [dimensionless]

        Returns
        -------
        rocd: float[]
            Rate of climb or descent [m/s]
            Defined as variation with time of the aircraft geopotential pressure
            altitude H_p
        """
        rocd = (
            (T - d_T) / T * (Thr - D) * V_tas * C_pow_red / m / self.__G_0 * f_M
        )
        return rocd

    def cal_tem_accel(
        self,
        T: array,
        d_T: array,
        m: array,
        D: array,
        rocd: array,
        Thr: array,
        V_tas: array,
    ) -> array:
        # NOTE: changed to equation  3.2-1
        """
        Total Energy Model. ROCD and Throttle Controller.
        (BADA User Menu Equation 3.2-1b and 3.2-7)
        Calculate accel given ROCD and thrust.

        Parameters
        ----------
        T: float[]
            Temperature [K]

        d_T: float[]
            Temperature differential at MSL [K]

        m: float[]
            Aircraft mass [kg]

        D: float[]
            Aerodynamic drag [N]

        rocd: float[]
            Rate of climb or descent [m/s]

        Thr: float[]
            Thrust acting parallel to the aircraft velocity vector [N]

        V_tas: float[]
            True airspeed [m/s]

        Returns
        -------
        accel: float[]
            Acceleration of tur air speed [m/s^2]
        """
        # return rocd / f_M / ((T-d_T)/T) * m*self.__G_0 / (Thr-D)
        return np.where(
            V_tas == 0,
            (Thr - D) / m,
            (Thr - D) / m - self.__G_0 / V_tas * rocd * T / (T - d_T),
        )

    def cal_tem_thrust(
        self,
        T: array,
        d_T: array,
        m: array,
        D: array,
        f_M: array,
        rocd: array,
        V_tas: array,
    ) -> array:
        # TODO: change to equation  3.2-1
        """
        Total Energy Model. Speed and ROCD Controller.
        (BADA User Menu Equation 3.2-1c and 3.2-7)
        Calculate thrust given ROCD and speed.

        Parameters
        ----------
        T: float[]
            Temperature [K]

        d_T: float[]
            Temperature differential at MSL [K]

        D: float[]
            Aerodynamic drag [N]

        m: float[]
            Aircraft mass [kg]

        f_M: float[]
            Energy share factor [dimenesionless]

        rocd: float[]
            Rate of climb or descent [m/s]

        V_tas: float[]
            True airspeed [m/s]

        Returns
        -------
        Thr: float[]
            Thrust acting parallel to the aircraft velocity vector [N]
        """
        Thr = rocd / f_M / ((T - d_T) / T) * m * self.__G_0 / V_tas + D
        return Thr

    def cal_vs_accel(
        self, traffic: "Traffic", tas: array
    ) -> tuple[array, array]:
        """
        Calculate vertical speed and acceleration given true airspeed.

        Parameters
        ----------
        traffic : traffic class
            Points to traffic array
        tas : float[]
            True airspeed [kt]

        Returns
        -------
        vs : float[]
            Vertical speed [ft/min]
        accel : float[]
            Acceleration [m/s^2]
        """
        if self.performance_mode == "BADA":
            # Drag and Thrust
            self.drag = self.perf_model.cal_aerodynamic_drag(
                tas,
                traffic.bank_angle,
                traffic.mass,
                traffic.weather.rho,
                traffic.configuration,
                self.perf_model.cal_expedite_descend_factor(
                    traffic.autopilot.expedite_descent
                ),
            )  # type: ignore
            self.thrust = self.perf_model.cal_thrust(
                traffic.vertical_mode,
                traffic.configuration,
                traffic.alt,
                traffic.tas,
                traffic.weather.d_T,
                self.drag,
                traffic.autopilot.speed_mode,
            )  # type: ignore
        else:
            self.drag = np.array(
                [
                    x.clean(
                        mass=traffic.mass[i],
                        tas=traffic.tas[i],
                        alt=traffic.alt[i],
                        path_angle=traffic.path_angle[i],
                    )
                    for i, x in enumerate(self.drag_model)
                ]
            )
            # drag.nonclean(mass=60000, tas=150, alt=100, flap_angle=20,
            # path_angle=10, landing_gear=True)
            self.thrust = np.array(
                [
                    x.cruise(tas=traffic.cas[i], alt=traffic.alt[i])
                    for i, x in enumerate(self.thrust_model)
                ]
            )
            thrust = []
            for i, x in enumerate(self.thrust_model):
                if (traffic.vertical_mode[i] == VerticalMode.CLIMB) | (
                    (traffic.vertical_mode[i] == VerticalMode.LEVEL)
                    & (
                        traffic.autopilot.speed_mode[i]
                        == APSpeedMode.ACCELERATE
                    )
                ):
                    thrust.append(
                        x.climb(
                            tas=traffic.tas[i], alt=traffic.alt[i], roc=1000
                        )
                    )
                elif (traffic.vertical_mode[i] == VerticalMode.LEVEL) & (
                    (
                        traffic.autopilot.speed_mode[i]
                        == APSpeedMode.CONSTANT_CAS
                    )
                    | (
                        traffic.autopilot.speed_mode[i]
                        == APSpeedMode.CONSTANT_MACH
                    )
                ):
                    thrust.append(self.drag[i])
                elif (traffic.vertical_mode[i] == VerticalMode.DESCENT) | (
                    (traffic.vertical_mode[i] == VerticalMode.LEVEL)
                    & (
                        traffic.autopilot.speed_mode[i]
                        == APSpeedMode.DECELERATE
                    )
                ):
                    thrust.append(
                        x.descent_idle(tas=traffic.tas[i], alt=traffic.alt[i])
                    )
            self.thrust = np.array(thrust)
            # T = thrust.takeoff(tas=100, alt=0) T = thrust.climb(
            # tas=200, alt=20000, roc=1000)

        # total energy model energy share factor
        self.esf = self.cal_energy_share_factor(
            Unit.ft2m(traffic.alt),
            traffic.weather.T,
            traffic.weather.d_T,
            traffic.mach,
            traffic.autopilot.speed_mode,
            traffic.vertical_mode,
        )  # type: ignore
        if self.performance_mode == "BADA":
            rocd = self.cal_tem_rocd(
                traffic.weather.T,
                traffic.weather.d_T,
                traffic.mass,
                self.drag,
                self.esf,
                self.thrust,
                tas,
                self.perf_model.cal_reduced_climb_power(
                    traffic.mass, traffic.alt, traffic.max_alt
                ),
            )
        else:
            rocd = self.cal_tem_rocd(
                traffic.weather.T,
                traffic.weather.d_T,
                traffic.mass,
                self.drag,
                self.esf,
                self.thrust,
                tas,
                np.ones_like(tas),
            )

        accel = np.where(
            (traffic.autopilot.speed_mode == APSpeedMode.ACCELERATE)
            | (traffic.autopilot.speed_mode == APSpeedMode.DECELERATE),
            self.cal_tem_accel(
                traffic.weather.T,
                traffic.weather.d_T,
                traffic.mass,
                self.drag,
                rocd,
                self.thrust,
                tas,
            ),
            0.0,
        )

        return Unit.mps2ftpm(rocd), accel

    def cal_fuel_burn(
        self, flight_phase: uint_array, tas: array, alt: array
    ) -> array:
        """
        Calculate fuel burn

        Parameters
        ----------
        flight_phase : float[]
            Flight phase from Traffic class [Flight_phase enum]
        tas : float[]
            True airspeed [kt]
        alt : float[]
            Altitude [ft]

        Returns
        -------
        Fuel burn : float[]
            Fuel burn [kg/s]
        """
        if self.performance_mode == "BADA":
            return self.perf_model.cal_fuel_burn(
                flight_phase, tas, self.thrust, alt
            )
        else:
            return np.array(
                [
                    x.at_thrust(acthr=self.thrust[i], alt=alt[i])
                    for i, x in enumerate(self.fuel_flow_model)
                ]
            )
        # FF = fuelflow.takeoff(tas=100, alt=0, throttle=1)
        # FF = fuelflow.enroute(mass=60000, tas=200, alt=20000, path_angle=3)
        # FF = fuelflow.enroute(mass=60000, tas=230, alt=32000, path_angle=0)

    ## TURNING
    def cal_rate_of_turn(self, bank_angle: array, V_tas: array) -> array:
        """
        Calculate rate of turn (Equation 5.3-1)

        Parameters
        ----------
        bank_angle: float[]
            Bank angle [deg]

        V_tas: float[]
            True air speed [m/s]

        Returns
        -------
        Rate of turn : float[]
            Rate of turn [deg/s]
        """
        rate_of_turn = np.rad2deg(
            self.__G_0 / V_tas * np.tan(np.deg2rad(bank_angle))
        )
        return rate_of_turn  # type: ignore

    def cal_bank_angle(self, rate_of_turn: array, V_tas: array) -> array:
        """
        Calculate rate of turn (Equation 5.3-1)

        Parameters
        ----------
        rate_of_turn: float[]
            Rate of turn [deg/s]

        V_tas: float[]
            True air speed [m/s]

        Returns
        -------
        bank_angle: float[]
            Bank angle [deg]
        """
        bank_angle = np.rad2deg(
            np.arctan(np.deg2rad(rate_of_turn) * V_tas / self.__G_0)
        )
        return bank_angle  # type: ignore

    def cal_turn_radius(self, bank_angle: array, V_tas: array) -> array:
        """
        Calculate rate of turn (Equation 5.3-1)

        Parameters
        ----------
        bank_angle: float[]
            Bank angle [deg]

        V_tas: float[]
            True air speed [m/s]

        Returns
        -------
        turn_radius: float[]
            Turn radius [m]
        """
        turn_radius = (
            np.square(V_tas) / self.__G_0 / np.tan(np.deg2rad(bank_angle))
        )
        return turn_radius  # type: ignore

    def get_bank_angles(self, configuration: uint_array) -> array:
        """
        Get standard nominal bank angles (Session 5.3)

        Parameters
        ----------
        configuration: float[]
            configuration from Traffic class [configuration enum]

        Returns
        -------
        bank_angles :float
            Bank angles [deg]
        """
        if self.performance_mode == "BADA":
            return np.where(
                (configuration == Config.TAKEOFF)
                | (configuration == Config.LANDING),
                self.perf_model._Bada__PHI_NORM_CIV_TOLD,  # type: ignore
                self.perf_model._Bada__PHI_NORM_CIV_OTHERS,  # type: ignore
                # FIXME(abrah): why access private???
            )
        else:
            return np.where(
                (configuration == Config.TAKEOFF)
                | (configuration == Config.LANDING),
                15.0,
                30.0,
            )

    def update_configuration(
        self, V_cas: array, H_p: array, vertical_mode: uint_array
    ) -> uint_array:
        """
        Update Flight Phase (section 3.5)

        V_cas: float[]
            True air speed [knots]

        H_p: float[]
            Geopotential pressuer altitude [ft]

        vertical_mode : float[]
            Vertical mode from Traffic class [Vertical_mode enum]

        Returns
        -------
        configuration : float[]
            configuration from Traffic class [configuration enum]
        """
        if self.performance_mode == "BADA":
            return self.perf_model.update_configuration(
                V_cas, H_p, vertical_mode
            )
        else:
            return np.where(V_cas > 0.0, Config.CLEAN, Config.TAKEOFF)
