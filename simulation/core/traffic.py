import numpy as np

from core.autopilot import Autopilot
from core.weather.weather import Weather
from core.performance.performance import Performance
from utils.unit import Unit_conversion
from utils.enums import Flight_phase, Speed_mode, AP_speed_mode, AP_throttle_mode, AP_vertical_mode, Configuration, Vertical_mode
from utils.cal import Calculation

class Traffic:

    def __init__(self, N, file_name, start_time, end_time, era5_weather=False, bada_perf=False):
        """
        Initialize base traffic array to store aircraft state variables for one timestep.

        file_name : String
            Output file name

        N :  int
            Total number of aircraft
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
        self.configuration = np.zeros([N])
        """Aircraft configuration [Configuration enum 1: Clean, 2: Take Off, 3: Approach, 4: Landing]"""
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
        self.cas = np.zeros([N])                                
        """Calibrated air speed [knot]"""
        self.tas = np.zeros([N])                                
        """True air speed [knot]"""
        self.gs_north = np.zeros([N])                           
        """Ground speed - North[knot]"""
        self.gs_east = np.zeros([N])                            
        """Ground speed - East [knot]  """
        self.mach = np.zeros([N])                               
        """Mach number [dimensionless]"""
        self.accel = np.zeros([N])
        """Acceleration [m/s^2]"""
        self.speed_mode = np.zeros([N])
        """Speed mode [Traffic.speed_mode enum 1: CAS, 2: MACH]"""

        # Vertical speed
        self.vs = np.zeros([N])                                 
        """Vertical speed [feet/min]"""
        self.fpa = np.zeros([N])                                
        """Flight path angle [deg]"""
        self.vertical_mode = np.zeros([N])
        """Vertical mode [Vertical mode enum 1: LEVEL, 2: CLIMB, 3: DESCENT]"""

        # Weight and balance
        self.mass = np.zeros([N])                               
        """Aircraft mass [kg]"""
        self.empty_weight = np.zeros(([N]))
        """Empty weight [kg]"""
        self.fuel_weight = np.zeros([N])                        
        """Initial fuel weight [kg]"""
        self.payload_weight = np.zeros([N])                     
        """Payload weight [kg]"""
        self.fuel_consumed = np.zeros([N])
        """Fuel consumped [kg]"""

        # Sub classes
        self.perf = Performance(N, bada_perf)                              
        """Performance class"""
        self.ap = Autopilot(N)                                  
        """Autopilot class"""
        self.weather = Weather(N, start_time, end_time, era5_weather, file_name)                               
        """Weather class"""

    
    def add_aircraft(self, call_sign, aircraft_type, flight_phase, configuration, lat, long, alt, heading, cas, fuel_weight, payload_weight, departure_runway, arrival_runway, flight_plan, target_speed, target_alt):
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

        
        # Add aircraft in performance, weather, and autopilot array
        self.perf.add_aircraft(n, aircraft_type)
        self.weather.add_aircraft(n, alt, self.perf)
        self.ap.add_aircraft(n, lat, long, alt, heading, cas, departure_runway, arrival_runway, flight_plan, target_speed, target_alt)

        # Initialize variables
        self.call_sign[n] = call_sign
        self.aircraft_type[n] = aircraft_type
        self.flight_phase[n] = flight_phase
        self.configuration[n] = configuration
        self.lat[n] = lat
        self.long[n] = long
        self.alt[n] = alt
        self.ap.alt[n] = alt
        self.heading[n] = heading
        self.ap.heading[n] = heading
        self.cas[n] = cas
        self.ap.cas[n] = cas
        self.tas[n] = Unit_conversion.mps_to_knots(self.perf.cas_to_tas(Unit_conversion.knots_to_mps(cas), self.weather.p[n], self.weather.rho[n]))
        self.mach[n] = self.perf.tas_to_mach(Unit_conversion.knots_to_mps(self.tas[n]), self.weather.T[n])
        self.empty_weight[n] = self.perf.get_empty_weight(n)
        self.fuel_weight[n] = fuel_weight
        self.payload_weight[n] = payload_weight
        self.mass[n] = self.empty_weight[n] + fuel_weight + payload_weight
        
         # Init Procedural speed
        self.perf.init_procedure_speed(self.mass, n)
        self.trans_alt = Unit_conversion.meter_to_feet(self.perf.cal_transition_alt(n, self.weather.d_T))

        # Increase aircraft count
        self.n = self.n + 1

        return n


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
        self.mass[n] = 0
        self.fuel_weight[n] = 0
        self.payload_weight[n] = 0
          
        self.perf.del_aircraft(n)

        # Decrease aircraft count
        self.n = self.n - 1
    

    
    def update(self, global_time, d_t = 1):
        """
        Update aircraft state for each timestep given ATC/autopilot command.

        Parameters
        ----------
        d_t: float
            delta time per timestep [s] TODO: need?

        Note
        ----
        """

        # print("Traffic.py - update()")

        # Update atmosphere
        self.weather.update(self.lat, self.long, self.alt, self.perf, global_time)

        # Ceiling
        self.max_alt = self.perf.cal_maximum_alt(self.weather.d_T, self.mass)   # TODO: calculate only once
        # min_speed = self.perf.cal_minimum_speed(self.flight_phase)
        # max_d_tas = self.perf.cal_max_d_tas(d_t)
        # max_d_rocd = self.perf.cal_max_d_rocd(d_t, self.unit.knots_to_mps(self.d_cas), tas, self.unit.ftpm_to_mps(self.vs))

        self.speed_mode = np.where(self.alt < self.trans_alt, Speed_mode.CAS, Speed_mode.MACH)

        # Update autopilot
        self.ap.update(self)

        # Bank angle
        d_heading = Calculation.cal_angle_diff(self.heading, self.ap.heading)
        self.bank_angle = np.select(condlist=[
                                        d_heading > 0.5,
                                        d_heading < -0.5,
                                    ],
                                    choicelist=[
                                        self.perf.get_bank_angles(self.flight_phase),                   # Turn right
                                        np.negative(self.perf.get_bank_angles(self.flight_phase))       # Turn left
                                    ],
                                    default = 0.0
                                )
                                
        tas = Unit_conversion.knots_to_mps(self.tas)   #TAS in m/s
        self.vs, self.accel = self.perf.cal_vs_accel(self, tas)
        
        # Air Speed
        # self.tas = self.perf.cas_to_tas(self.cas, self.weather.p, self.weather.rho)
        tas = tas + self.accel
        self.mach = self.perf.tas_to_mach(tas, self.weather.T)       
        self.cas = Unit_conversion.mps_to_knots(self.perf.tas_to_cas(tas, self.weather.p, self.weather.rho))

        # Bound to autopilot
        self.mach = np.select(condlist=[
                                (self.speed_mode == Speed_mode.MACH) & (self.ap.speed_mode == AP_speed_mode.ACCELERATE),
                                (self.speed_mode == Speed_mode.MACH) & (self.ap.speed_mode == AP_speed_mode.DECELERATE),
                                (self.speed_mode == Speed_mode.MACH) & (self.ap.speed_mode == AP_speed_mode.CONSTANT_MACH)
                            ],
                            choicelist=[
                                np.where(self.mach > self.ap.mach, self.ap.mach, self.mach),
                                np.where(self.mach < self.ap.mach, self.ap.mach, self.mach),
                                self.ap.mach
                            ],
                            default=self.mach)

        self.cas = np.select(condlist=[
                                (self.speed_mode == Speed_mode.CAS) & (self.ap.speed_mode == AP_speed_mode.ACCELERATE),
                                (self.speed_mode == Speed_mode.CAS) & (self.ap.speed_mode == AP_speed_mode.DECELERATE),
                                (self.speed_mode == Speed_mode.CAS) & (self.ap.speed_mode == AP_speed_mode.CONSTANT_CAS)
                            ],
                            choicelist=[
                                np.where(self.cas > self.ap.cas, self.ap.cas, self.cas),    #TODO: change to minimum
                                np.where(self.cas < self.ap.cas, self.ap.cas, self.cas),
                                self.ap.cas
                            ],
                            default=self.cas)

        tas = np.select(condlist=[
                            self.ap.speed_mode == AP_speed_mode.CONSTANT_MACH,
                            self.ap.speed_mode == AP_speed_mode.CONSTANT_CAS
                        ],
                        choicelist=[
                            self.perf.mach_to_tas(self.mach, self.weather.T),
                            self.perf.cas_to_tas(Unit_conversion.knots_to_mps(self.cas), self.weather.p, self.weather.rho)
                        ],
                        default=tas)

        tas = np.select(condlist=[
                            (self.speed_mode == Speed_mode.CAS) & ((self.ap.speed_mode == AP_speed_mode.ACCELERATE) | (self.ap.speed_mode == AP_speed_mode.DECELERATE)) & (self.cas == self.ap.cas),
                            (self.speed_mode == Speed_mode.MACH) & ((self.ap.speed_mode == AP_speed_mode.ACCELERATE) | (self.ap.speed_mode == AP_speed_mode.DECELERATE)) & (self.mach == self.ap.mach)
                        ],
                        choicelist=[
                            self.perf.cas_to_tas(Unit_conversion.knots_to_mps(self.cas), self.weather.p, self.weather.rho),
                            self.perf.mach_to_tas(self.mach, self.weather.T)
                        ],
                        default=tas)

        self.mach = np.where((self.speed_mode == Speed_mode.CAS) & ((self.ap.speed_mode == AP_speed_mode.ACCELERATE) | (self.ap.speed_mode == AP_speed_mode.DECELERATE)) & (self.cas == self.ap.cas), 
                                self.perf.tas_to_mach(tas, self.weather.T),
                                self.mach)
        
        self.cas = np.where((self.speed_mode == Speed_mode.MACH) & ((self.ap.speed_mode == AP_speed_mode.ACCELERATE) | (self.ap.speed_mode == AP_speed_mode.DECELERATE)) & (self.mach == self.ap.mach),
                                Unit_conversion.mps_to_knots(self.perf.tas_to_cas(tas, self.weather.p, self.weather.rho)),
                                self.cas)

        self.tas = Unit_conversion.mps_to_knots(tas) 


        # Heading
        rate_of_turn = self.perf.cal_rate_of_turn(self.bank_angle, tas)     # TODO: https://skybrary.aero/articles/rate-turn
        self.heading = np.where((np.abs(d_heading) < np.abs(rate_of_turn)) | (np.abs(d_heading) < 0.5), self.ap.heading, self.heading + rate_of_turn)
        self.heading = np.select(condlist=[
                                    self.heading > 360.0,
                                    self.heading < 0.0
                                ],
                                choicelist=[
                                    self.heading - 360.0,
                                    self.heading + 360.0
                                ],
                                default=self.heading)
        
        # Ground speed
        self.gs_north = self.tas * np.cos(np.deg2rad(self.heading)) + self.weather.wind_north
        self.gs_east = self.tas * np.sin(np.deg2rad(self.heading)) + self.weather.wind_east

        # Position
        self.lat = self.lat + self.gs_north / 216000.0
        self.long = self.long + self.gs_east / 216000.0
        self.alt = self.alt + self.vs / 60.0
        self.alt = np.select(condlist=[     #handle overshoot
                                self.vertical_mode == Vertical_mode.CLIMB,
                                self.vertical_mode == Vertical_mode.DESCENT
                            ],
                            choicelist=[
                                np.where(self.alt > self.ap.alt, self.ap.alt, self.alt),
                                np.where(self.alt < self.ap.alt, self.ap.alt, self.alt)
                            ],
                            default=self.alt)

        # Fuel        
        fuel_burn = self.perf.cal_fuel_burn(self.flight_phase, self.tas, self.alt) 
        self.fuel_consumed = self.fuel_consumed + fuel_burn
        self.mass = self.mass - fuel_burn

        # Flight phase and configuration
        # Take off -> climb
        self.flight_phase = np.where((self.flight_phase == Flight_phase.TAKEOFF) & (self.alt > 1500.0), Flight_phase.CLIMB, self.flight_phase)
        self.flight_phase = np.where((self.flight_phase != Flight_phase.TAKEOFF) & (self.vertical_mode == Vertical_mode.CLIMB), Flight_phase.CLIMB, self.flight_phase)
        # Climb -> Cruise
        self.flight_phase = np.where(self.vertical_mode == Vertical_mode.LEVEL, Flight_phase.CRUISE, self.flight_phase)         #TODO: Or use cruise altitude?
        # Cruise-Descent
        self.flight_phase = np.where(self.vertical_mode == Vertical_mode.DESCENT, Flight_phase.DESCENT, self.flight_phase)