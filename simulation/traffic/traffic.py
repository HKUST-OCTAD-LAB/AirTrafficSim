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
        """Vertical speed [feet/s]"""
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
    

    
    def update(self, d_t, i = -1 ):
        """
        Update aircraft state for each timestep given ATC/autopilot command.

        Parameters
        ----------
        d_t: float
            delta time per timestep [s]

        i: int
            Index of the specific aircraft to undergo calculation. If undefined, update will calculate all aircraft

        Note
        ----
        TODO: Index
        """

        print("Traffic.py - update()")

        # if (i == -1):
        #     i = 0
        #     n = self.n      # Set number of aircraft to be total number
        # else:
        #     n = i + 1
        
        # # Turn (assume standard 3 deg/s turn)
        # print("Set heading:", self.ap.heading[i:n])

        # if(self.ap.heading[i:n] - self.heading[i:n] > 3):
        #     self.heading[i:n] += 3
        # elif(self.ap.heading[i:n] - self.heading[i:n] < -3):
        #     self.heading[i:n] -= 3
        # else:
        #     self.heading[i:n] = self.ap.heading[i:n]

        # if (self.heading[i:n] > 360):
        #     self.heading[i:n] = self.heading[i:n] - 360
        # if (self.heading[i:n] < 0):
        #     self.heading[i:n] = 360 + self.heading[i:n]

        # # self.ap_rate_of_turn = rate_of_turn
        # print("Current heading:", self.heading[i:n])

        # # Calculate ground speed
        # self.gs_north[i:n] = self.tas[i:n] * np.cos(np.deg2rad(self.heading[i:n])) + self.weather.wind_north[i:n]
        # self.gs_east[i:n] = self.tas[i:n] * np.sin(np.deg2rad(self.heading[i:n])) + self.weather.wind_east[i:n]
        # print("Ground speed: (North/East)", self.gs_north[i:n], self.gs_east[i:n])

        # # Calculate position
        # self.lat[i:n] = self.lat[i:n] + self.gs_north[i:n] / 216000
        # self.long[i:n] = self.long[i:n] + self.gs_east[i:n] / 216000
        # print("Position: ", self.lat[i:n], self.long[i:n])

        # Update atmosphere
        self.weather.T = self.perf.cal_temperature(self.alt, self.weather.d_T)
        self.weather.p = self.perf.cal_air_pressure(self.alt, self.weather.T, self.weather.d_T)
        self.weather.rho = self.perf.cal_air_density(self.weather.p, self.weather.T)

        # Ceiling
        max_alt = self.perf.cal_maximum_altitude(self.weather.d_T, self.mass)   # TODO: calculate only once
        min_speed = self.perf.cal_minimum_speed(self.flight_phase)
        max_d_tas = self.perf.cal_max_d_tas(d_t)
        max_d_rocd = self.perf.cal_max_d_rocd(d_t, self.unit.knots_to_mps(self.d_cas), self.unit.knots_to_mps(self.tas), self.unit.feet_to_meter(self.vs))

        # Procedure
        h_p_trans = self.perf.cal_transition_alt(self.unit.knots_to_mps(self.cas), self.mach, self.weather.d_T)
        # After transiiont altitude, constant mach 
        self.perf.get_procedure_speed(self.unit.feet_to_meter(self.alt), h_p_trans, self.flight_phase)

        # Air Speed
        self.cas = self.perf.cal_speed_of_sound
        self.tas = self.perf.cas_to_tas(self.cas, self.weather.p, self.weather.rho)
        self.mach = self.perf.tas_to_mach(self.tas, self.weather.T)

        # Heading
        self.perf.cal_rate_of_turn(self.bank_angle, self.unit.knots_to_mps(self.tas))

        # Thrust and drag
        self.drag = self.perf.cal_aerodynamic_drag(self.tas, self.bank_angle, self.mass, self.weather.rho, self.flight_phase, self.perf.cal_expedite_descend_factor(self.ap.expedite_descent))
       
        self.thrust = np.select(condlist=[self.flight_phase <= Flight_phase.CLIMB,
                                         self.flight_phase == Flight_phase.CRUISE,
                                         self.flight_phase >= Flight_phase.DESCENT],
                                choicelist=[self.perf.cal_max_climb_to_thrust(self.alt, self.tas, self.weather.d_T),
                                            np.minimum(self.drag, self.perf.cal_max_cruise_thrust(self.perf.cal_max_climb_to_thrust(self.alt, self.tas, self.weather.d_T))),         #T = D at cruise, but limited at max cruise thrust
                                            self.perf.cal_descent_thrust(self.alt, self.perf.cal_max_climb_to_thrust(self.alt, self.tas, self.weather.d_T), self.configuration)])

        # Total Energy Model
        self.esf = self.perf.cal_energy_share_factor(self.alt, self.weather.T, self.weather.d_T, self.mach, self.ap.speed_mode, self.flight_phase)      # Energy share factor

        # Thrust mode
        # self.thrust = self.perf.cal_tem_thrust(self.weather.T, self.weather.d_T, self.drag, self.mass, self.esf, self.unit.feet_to_meter(self.vs), self.unit.knots_to_mps(self.tas))      #TODO: VNAV?

        # Speed mode
        self.vs = np.where(self.ap.vertical_mode == AP_vertical_mode.FLC,
                            Unit_conversion.meter_to_feet(self.perf.cal_tem_rocd(self.weather.T, self.weather.d_T, self.mass, self.drag, self.esf, self.thrust, self.unit.knots_to_mps(self.tas), self.perf.cal_reduced_climb_power(self.mass, self.alt, max_alt))),
                            self.vs)

        self.tas = np.where(self.ap.vertical_mode == AP_vertical_mode.VS, 
                            Unit_conversion.mps_to_knots(self.perf.cal_tem_speed(self.weather.T, self.weather.d_T, self.mass, self.drag, self.esf, self.unit.feet_to_meter(self.vs), self.thrust)),
                            self.tas)

                    
        
        # Ground speed and position
        self.gs_north = self.tas * np.cos(np.deg2rad(self.heading)) + self.weather.wind_north
        self.gs_east = self.tas * np.sin(np.deg2rad(self.heading)) + self.weather.wind_east
        self.lat = self.lat + self.gs_north / 216000.0
        self.long = self.long + self.gs_east / 216000.0
        self.alt = self.alt + self.vs

        # Fuel
        fuel_flow = np.select(condlist=[self.flight_phase == Flight_phase.CRUISE,
                                        self.flight_phase == Flight_phase.DESCENT,
                                        self.flight_phase == Flight_phase.APPROACH,
                                        self.flight_phase == Flight_phase.LANDING], 
                            choicelist=[self.perf.cal_cruise_fuel_flow(self.tas, self.thrust),                         # cruise
                                        self.perf.cal_minimum_fuel_flow(self.alt),                                     # Idle descent
                                        self.perf.cal_approach_landing_fuel_flow(self.tas, self.thrust, self.alt),     # Approach
                                        self.perf.cal_approach_landing_fuel_flow(self.tas, self.thrust, self.alt)],    # Landing                        
                            default=self.perf.cal_nominal_fuel_flow(self.tas, self.thrust)                             # Others
                            )   #TODO: unit kg/min? input second?
        self.fuel_weight = self.fuel_weight - fuel_flow/60.0

        # Update flight phase


    def save(self, writer, time):
            data = np.column_stack((np.full(self.n, time), np.arange(self.n), self.call_sign[:self.n], self.lat[:self.n], self.long[:self.n], self.alt[:self.n], self.heading[:self.n], self.cas[:self.n]))
            writer.writerows(data)
