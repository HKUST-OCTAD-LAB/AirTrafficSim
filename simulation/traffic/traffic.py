import numpy as np
import csv

from traffic.autopilot import Autopilot
from traffic.weather import Weather
from traffic.performance import Performance
from utils.unit import Unit_conversion
from utils.enums import Flight_phase, Engine_type, Wake_category, AP_speed_mode, AP_throttle_mode, AP_vertical_mode

class Traffic:

    def __init__(self, N=1000):
        """
        Initialize base traffic array to store aircraft state variables for one timestep.
        """

        # Memory and index control vairable:
        self.n = 0                                              
        """Aircraft count"""
        self.N = N                                              
        """Maximum aircraft count"""
        self.index = np.zeros([N])                              
        """Index array to indicate whether there is an aircraft active in each index."""

        # General information
        self.call_sign = np.empty([N], dtype='U10')             
        """Callsign [string]"""
        self.aircraft_type = np.empty([N], dtype='U4')          
        """Aircraft type in ICAO format [string]"""
        self.flight_phase = np.zeros([N])                       
        """Flight phase [Flight_phase enum] (BADA section 3.5)"""

        # Position
        self.lat = np.zeros([N])                                
        """Latitude [deg]"""
        self.long = np.zeros([N])                               
        """Longitude [deg]"""
        self.alt = np.zeros([N])                                
        """Altitude [ft] Geopotential altitude"""
        self.trans_alt = np.zeros([N])
        """Transaition altitude [ft]"""

        # Orientation
        self.heading = np.zeros([N])                            
        """Heading [deg]"""
        self.track_angle = np.zeros([N])                        
        """Track angle [deg]"""
        self.bank_angle = np.zeros([N])                         
        """Bank angle [deg]"""

        # Speed
        self.ias = np.zeros([N])                                
        """Indicated air speed [knot]"""
        self.cas = np.zeros([N])                                
        """Calibrated air speed [knot]"""
        self.d_cas = np.zeros([N])                              
        """Delta velocity [knot]"""
        self.tas = np.zeros([N])                                
        """True air speed [knot]"""
        self.gs_north = np.zeros([N])                           
        """Ground speed - North[knot]"""
        self.gs_east = np.zeros([N])                            
        """Ground speed - East [knot]  """
        self.mach = np.zeros([N])                               
        """Mach number [dimensionless]"""

        # Vertical speed
        self.vs = np.zeros([N])                                 
        """Vertical speed [feet/min]"""
        self.fpa = np.zeros([N])                                
        """Flight path angle [deg]"""

        # Aerodynamic
        self.drag = np.zeros([N])                               
        """Drag [N]"""
        self.esf = np.zeros([N])                                
        """Energy share factor [dimensionless]"""
        self.thrust = np.zeros([N])
        """Thrust [N]"""

        # Weight and balance
        self.mass = np.zeros([N])                               
        """Aircraft mass [kg]"""
        self.fuel_weight = np.zeros([N])                        
        """Fuel weight [kg]"""
        self.payload_weight = np.zeros([N])                     
        """Payload weight [kg]"""

        # Sub classes
        self.perf = Performance(N)                              
        """Performance class"""
        self.ap = Autopilot(N)                                  
        """Autopilot class"""
        self.weather = Weather(N)                               
        """Weather class"""
        self.unit = Unit_conversion()                
        """Unit conversion utils class"""

    
    def add_aircraft(self, call_sign, aircraft_type, flight_phase, lat, long, alt, heading, tas, weight, fuel_weight, payload_weight):
        """
        Add an aircraft to traffic array.

        Returns
        -------
        self.n-1: int
            Index of the added aircraft
        """

        print("Traffic.py - add_aircraft()", call_sign, " Type:",  aircraft_type)

        if (self.n >= self.N):
            # If new index exit maximum aircraft count
            new_index = np.argwhere(self.index == 0).flatten()
            if (new_index.size == 0):
                print ("Traffic array is full. Cannot add aircraft.")
                return -1
            else:
                # Assign new index from empty slots.
                n = new_index[0]
        else:
            n = self.n

        # Initialize variables
        self.call_sign[n] = call_sign
        self.aircraft_type[n] = aircraft_type
        self.flight_phase[n] = flight_phase
        self.lat[n] = lat
        self.long[n] = long
        self.alt[n] = alt
        self.heading[n] = heading
        self.tas[n] = tas
        self.weight[n] = weight
        self.fuel_weight[n] = fuel_weight
        self.payload_weight[n] = payload_weight

        # Add aircraft in performance array
        self.perf.add_aircraft(aircraft_type, n)
        
        # Increase aircraft count
        self.n = self.n + 1

        return self.n - 1


    def del_aircraft(self, n):
        """
        Delete an aircraft from traffic array.
        TODO:
        """
        self.index[n] = 0

        self.call_sign[n] = ''
        self.aircraft_type[n] = ''
        self.flight_phase[n] = 0
        self.lat[n] = 0
        self.long[n] = 0
        self.alt[n] = 0
        self.heading[n] = 0
        self.tas[n] = 0
        self.weight[n] = 0
        self.fuel_weight[n] = 0
        self.payload_weight[n] = 0
          
        self.perf.del_aircraft(n)
    

    
    def update(self, d_t = 1):
        """
        Update aircraft state for each timestep given ATC/autopilot command.

        Parameters
        ----------
        d_t: float
            delta time per timestep [s] TODO: need?

        Note
        ----
        """

        print("Traffic.py - update()")
        # Update atmosphere
        self.weather.update(self.perf)

        # Procedure
        self.trans_alt = self.perf.cal_transition_alt(self.unit.knots_to_mps(self.cas), self.mach, self.weather.d_T)
        # After transiiont altitude, constant mach 
        self.perf.get_procedure_speed(self.unit.feet_to_meter(self.alt), self.trans_alt, self.flight_phase)
        # Auto pilot target speed

        # Bank angle and Heading
        diff = np.mod(self.ap.heading - self.heading + 180.0, 360.0) - 180.0  
        self.bank_angle = np.select(condlist=[
                                        diff == 0.0,
                                        diff > 0,
                                        diff < 0,
                                    ],
                                    choicelist=[
                                        0.0,
                                        self.perf.get_nominal_bank_angles(self.flight_phase),                   # Turn right
                                        np.negative(self.perf.get_nominal_bank_angles(self.flight_phase))       # Turn left
                                    ]
                                )
        rate_of_turn = self.perf.cal_rate_of_turn(self.bank_angle, self.unit.knots_to_mps(self.tas))
        self.heading = np.where(np.abs(diff) < rate_of_turn, self.ap.heading, self.heading + rate_of_turn)
        self.heading = np.select(condlist=[
                                    self.heading > 360.0,
                                    self.heading < 0.0
                                ],
                                choicelist=[
                                    self.heading - 360.0,
                                    self.heading + 360.0
                                ],
                                default=self.heading)

        # Drag and Thrust
        self.drag = self.perf.cal_aerodynamic_drag(self.tas, self.bank_angle, self.mass, self.weather.rho, self.flight_phase, self.perf.cal_expedite_descend_factor(self.ap.expedite_descent))
       
        self.thrust = np.select(condlist=[
                                    self.flight_phase <= Flight_phase.CLIMB,
                                    self.flight_phase == Flight_phase.CRUISE,
                                    self.flight_phase >= Flight_phase.DESCENT],
                                choicelist=[
                                    self.perf.cal_max_climb_to_thrust(self.alt, self.tas, self.weather.d_T),
                                    np.minimum(self.drag, self.perf.cal_max_cruise_thrust(self.perf.cal_max_climb_to_thrust(self.alt, self.tas, self.weather.d_T))),         #T = D at cruise, but limited at max cruise thrust
                                        self.perf.cal_descent_thrust(self.alt, self.perf.cal_max_climb_to_thrust(self.alt, self.tas, self.weather.d_T), self.configuration)])

        # Total Energy Model
        self.esf = self.perf.cal_energy_share_factor(self.alt, self.weather.T, self.weather.d_T, self.mach, self.ap.speed_mode, self.flight_phase)      # Energy share factor

        # Thrust mode
        # self.thrust = self.perf.cal_tem_thrust(self.weather.T, self.weather.d_T, self.drag, self.mass, self.esf, self.unit.feet_to_meter(self.vs), self.unit.knots_to_mps(self.tas))      #TODO: VNAV?

        # Speed mode
        self.vs = np.where(self.ap.vertical_mode == AP_vertical_mode.FLC,
                            Unit_conversion.mps_to_ftpm(self.perf.cal_tem_rocd(self.weather.T, self.weather.d_T, self.mass, self.drag, self.esf, self.thrust, self.unit.knots_to_mps(self.tas), self.perf.cal_reduced_climb_power(self.mass, self.alt, max_alt))),
                            self.vs)

        self.tas = np.where(self.ap.vertical_mode == AP_vertical_mode.VS, 
                            Unit_conversion.mps_to_knots(self.perf.cal_tem_speed(self.weather.T, self.weather.d_T, self.mass, self.drag, self.esf, self.unit.ftpm_to_mps(self.vs), self.thrust)),
                            self.tas)

        # Ceiling
        max_alt = self.perf.cal_maximum_altitude(self.weather.d_T, self.mass)   # TODO: calculate only once
        min_speed = self.perf.cal_minimum_speed(self.flight_phase)
        max_d_tas = self.perf.cal_max_d_tas(d_t)
        max_d_rocd = self.perf.cal_max_d_rocd(d_t, self.unit.knots_to_mps(self.d_cas), self.unit.knots_to_mps(self.tas), self.unit.ftpm_to_mps(self.vs))


        # Air Speed
        self.tas = self.perf.cas_to_tas(self.cas, self.weather.p, self.weather.rho)
        self.mach = self.perf.tas_to_mach(self.tas, self.weather.T)       
        self.cas = Unit_conversion.mps_to_knots(self.perf.tas_to_cas(self.tas, self.weather.p, self.weather.rho))

        # Fuel                  
        self.fuel_weight = self.fuel_weight - self.perf.update_fuel(self.flight_phase, self.tas, self.thrust, self.alt) 
        
        # Ground speed
        self.gs_north = self.tas * np.cos(np.deg2rad(self.heading)) + self.weather.wind_north
        self.gs_east = self.tas * np.sin(np.deg2rad(self.heading)) + self.weather.wind_east

        # Position
        self.lat = self.lat + self.gs_north / 216000.0
        self.long = self.long + self.gs_east / 216000.0
        self.alt = self.alt + self.vs / 60.0


    def save(self, writer, time):
            data = np.column_stack((np.full(self.n, time), np.arange(self.n), self.call_sign[:self.n], self.lat[:self.n], self.long[:self.n], self.alt[:self.n], self.heading[:self.n], self.cas[:self.n]))
            writer.writerows(data)
