import numpy as np

from airtrafficsim.core.autopilot import Autopilot
from airtrafficsim.core.weather.weather import Weather
from airtrafficsim.core.performance.performance import Performance
from airtrafficsim.utils.unit_conversion import Unit
from airtrafficsim.utils.enums import FlightPhase, SpeedMode, APSpeedMode, APThrottleMode, APVerticalMode, Config, VerticalMode
from airtrafficsim.utils.calculation import Cal

class Traffic:
    def __init__(self, file_name, start_time, end_time, era5_weather=False, bada_perf=False):
        """
        Initialize base traffic array to store aircraft state variables for one timestep.

        Parameters
        ----------
        file_name : String
            Output file name
        N :  int
            Total number of aircraft
        """

        # Memory and index control vairable:
        self.n = 0
        """Aircraft count"""
        # self.N = N                                              
        # """Maximum aircraft count"""

        # self.df = np.empty([0], dtype=[
        #     ('index', 'i8'), ('callsign', 'U10'), ('type', 'U4'), ('configuration', 'i8'), ('flight_phase', 'i8'), 
        #     ('lat', 'f8'), ('long', 'f8'), ('alt', 'f8'), ('trans_alt', 'f8'), 
        #     ('heading', 'f8'), ('track_angle', 'f8'), ('bank_angle', 'f8'), ('path_angle', 'f8'),
        #     ('cas', 'f8'), ('tas', 'f8'), ('gs_north', 'f8'), ('gs_east', 'f8'), ('mach', 'f8'), ('accel', 'f8'), ('speed_mode', 'i8'),
        #     ('max_alt', 'f8'), ('max_cas', 'f8'), ('max_mach', 'f8'),
        #     ('vs', 'f8'), ('fpa', 'f8'), ('vertical_mode', 'i8'),
        #     ('mass', 'f8'), ('empty_weight', 'f8'), ('fuel_weight', 'f8'), ('payload_weight', 'f8'), ('fuel_consumed', 'f8'),
        #     # Autopilot
        #     ('ap_alt', 'f8'), ('ap_heading', 'f8'), ('ap_track_angle', 'f8'), ('ap_rate_of_turn', 'f8'),
        #     ('ap_cas', 'f8'), ('ap_mach', 'f8'), ('ap_vs', 'f8'), ('ap_fpa', 'f8'), 
        #     ('ap_lat', 'f8'), ('ap_long', 'f8'), ('ap_lat_next', 'f8'), ('ap_long_next', 'f8'), ('ap_hv_next_wp', '?'), ('ap_dist_wp', 'f8')
        #     ('ap_flight_plan_index', 'i8'), ('ap_procedure_speed', 'f8')
        #     # Weather
        #     ('wind_speed', 'f8'), ('wind_dir', 'f8'), ('wind_north', 'f8'), ('wind_east', 'f8'),
        #     ('d_T', 'f8'), ('d_p', 'f8'), ('T', 'f8'), ('p', 'f8'), ('rho', 'f8')
        # ])

        self.index = np.zeros([0])                              
        """Index array to indicate whether there is an aircraft active in each index."""

        # General information
        self.call_sign = np.empty([0], dtype='U10')             
        """Callsign [string]"""
        self.aircraft_type = np.empty([0], dtype='U4')          
        """Aircraft type in ICAO format [string]"""
        self.configuration = np.zeros([0])
        """Aircraft configuration [Configuration enum 1: Clean, 2: Take Off, 3: Approach, 4: Landing]"""
        self.flight_phase = np.zeros([0])                       
        """Flight phase [Flight_phase enum] (BADA section 3.5)"""

        # Position
        self.lat = np.zeros([0])                                
        """Latitude [deg]"""
        self.long = np.zeros([0])                               
        """Longitude [deg]"""
        self.alt = np.zeros([0])                                
        """Altitude [ft] Geopotential altitude"""
        self.trans_alt = np.zeros([0])
        """Transaition altitude [ft]"""
        self.cruise_alt = np.zeros([0])
        """Cruise altitude [ft]"""

        # Orientation
        self.heading = np.zeros([0])                            
        """Heading [deg]"""
        self.track_angle = np.zeros([0])                        
        """Track angle [deg]"""
        self.bank_angle = np.zeros([0])                         
        """Bank angle [deg]"""
        self.path_angle = np.zeros([0])
        """Path angle [deg]"""

        # Speed
        self.cas = np.zeros([0])                                
        """Calibrated air speed [knot]"""
        self.tas = np.zeros([0])                                
        """True air speed [knot]"""
        self.gs_north = np.zeros([0])                           
        """Ground speed - North[knot]"""
        self.gs_east = np.zeros([0])                            
        """Ground speed - East [knot]  """
        self.mach = np.zeros([0])                               
        """Mach number [dimensionless]"""
        self.accel = np.zeros([0])
        """Acceleration [m/s^2]"""
        self.speed_mode = np.zeros([0])
        """Speed mode [Traffic.speed_mode enum 1: CAS, 2: MACH]"""

        # Ceiling
        self.max_alt = np.zeros([0])
        """Maximum altitude [feet]"""
        self.max_cas = np.zeros([0])
        """Maximum calibrated air speed [knot]"""
        self.max_mach = np.zeros([0])
        """Maximum mach number [dimensionless]"""

        # Vertical speed
        self.vs = np.zeros([0])                                 
        """Vertical speed [feet/min]"""
        self.fpa = np.zeros([0])                                
        """Flight path angle [deg]"""
        self.vertical_mode = np.zeros([0])
        """Vertical mode [Vertical mode enum 1: LEVEL, 2: CLIMB, 3: DESCENT]"""

        # Weight and balance
        self.mass = np.zeros([0])                               
        """Aircraft mass [kg]"""
        self.empty_weight = np.zeros([0])
        """Empty weight [kg]"""
        self.fuel_weight = np.zeros([0])                        
        """Initial fuel weight [kg]"""
        self.payload_weight = np.zeros([0])                     
        """Payload weight [kg]"""
        self.fuel_consumed = np.zeros([0])
        """Fuel consumped [kg]"""

        # Sub classes
        self.perf = Performance(bada_perf)                              
        """Performance class"""
        self.ap = Autopilot()                                  
        """Autopilot class"""
        self.weather = Weather(start_time, end_time, era5_weather, file_name)                               
        """Weather class"""

    
    def add_aircraft(self, call_sign, aircraft_type, flight_phase, configuration, lat, long, alt, heading, cas, fuel_weight, payload_weight, departure_airport, departure_runway, sid, arrival_airport, arrival_runway, star, approach, flight_plan, cruise_alt):
        """
        Add an aircraft to traffic array.

        Returns
        -------
        self.n-1: int
            Index of the added aircraft
        """

        print("Traffic.py - add_aircraft()", call_sign, " Type:",  aircraft_type)
        
        # Add aircraft in performance, weather, and autopilot array
        self.perf.add_aircraft(aircraft_type)
        self.weather.add_aircraft(alt, self.perf)
        self.ap.add_aircraft(lat, long, alt, heading, cas, departure_airport, departure_runway, sid, arrival_airport, arrival_runway, star, approach, flight_plan, cruise_alt)

        self.index = np.append(self.index, self.n)
        self.call_sign = np.append(self.call_sign, call_sign)             
        self.aircraft_type = np.append(self.aircraft_type, aircraft_type)          
        self.configuration = np.append(self.configuration, configuration)
        self.flight_phase = np.append(self.flight_phase, flight_phase)                      
        self.lat = np.append(self.lat, lat)                               
        self.long = np.append(self.long, long)                              
        self.alt = np.append(self.alt, alt)                              
        self.cruise_alt = np.append(self.cruise_alt, cruise_alt)
        self.heading = np.append(self.heading, heading)                          
        self.track_angle = np.append(self.track_angle, heading)                       
        self.bank_angle = np.append(self.bank_angle, 0.0)                       
        self.path_angle = np.append(self.path_angle, 0.0)
        self.cas = np.append(self.cas, cas)                               
        self.tas = np.append(self.tas, Unit.mps2kts(self.perf.cas_to_tas(Unit.kts2mps(cas), self.weather.p[-1], self.weather.rho[-1])))
        self.gs_north = np.append(self.gs_north, 0.0)                          
        self.gs_east = np.append(self.gs_east, 0.0)                            
        self.mach = np.append(self.mach, self.perf.tas_to_mach(Unit.kts2mps(self.tas[-1]), self.weather.T[-1]))
        self.accel = np.append(self.accel, 0.0)
        self.speed_mode = np.append(self.speed_mode, SpeedMode.CAS)
        self.max_alt = np.append(self.max_alt, 0.0)
        self.max_cas = np.append(self.max_cas, 0.0)
        self.max_mach = np.append(self.max_mach, 0.0)
        self.vs = np.append(self.vs, 0.0)                               
        self.fpa = np.append(self.fpa, 0.0)                               
        self.vertical_mode = np.append(self.vertical_mode, VerticalMode.LEVEL)
        self.empty_weight = np.append(self.empty_weight, self.perf.get_empty_weight(-1))
        self.fuel_weight = np.append(self.fuel_weight, fuel_weight)                     
        self.payload_weight = np.append(self.payload_weight, payload_weight)
        self.mass = np.append(self.mass, self.empty_weight[-1] + fuel_weight + payload_weight)                  
        self.fuel_consumed = np.append(self.fuel_consumed, 0.0)

        # Init Procedural speed
        self.perf.init_procedure_speed(self.mass[-1], -1)
        self.trans_alt = np.append(self.trans_alt, Unit.m2ft(self.perf.cal_transition_alt(-1, self.weather.d_T[-1])))

        self.max_alt = self.perf.cal_maximum_alt(self.weather.d_T, self.mass)
        self.max_cas, self.max_mach = self.perf.cal_maximum_speed()
        
        # Increase aircraft count
        self.n = self.n + 1

        return self.n - 1


    def del_aircraft(self, index):
        """
        Delete an aircraft from traffic array.

        Parameters
        ----------
        index : int
            Index of an aircraft
        """
        print("Traffic.py - del_aircraft()", index)
        i = np.where(self.index == index)[0][0]
        self.index = np.delete(self.index, i)                      
        self.call_sign = np.delete(self.call_sign, i)             
        self.aircraft_type = np.delete(self.aircraft_type, i)          
        self.configuration = np.delete(self.configuration, i)
        self.flight_phase = np.delete(self.flight_phase, i)                      
        self.lat = np.delete(self.lat, i)                               
        self.long = np.delete(self.long, i)                              
        self.alt = np.delete(self.alt, i)                              
        self.trans_alt = np.delete(self.trans_alt, i)
        self.cruise_alt = np.delete(self.cruise_alt, i)
        self.heading = np.delete(self.heading, i)                          
        self.track_angle = np.delete(self.track_angle, i)                       
        self.bank_angle = np.delete(self.bank_angle, i)                       
        self.path_angle = np.delete(self.path_angle, i)
        self.cas = np.delete(self.cas, i)                               
        self.tas = np.delete(self.tas, i)                                
        self.gs_north = np.delete(self.gs_north, i)                          
        self.gs_east = np.delete(self.gs_east, i)                            
        self.mach = np.delete(self.mach, i)                               
        self.accel = np.delete(self.accel, i)
        self.speed_mode = np.delete(self.speed_mode, i)
        self.max_alt = np.delete(self.max_alt, i)
        self.max_cas = np.delete(self.max_cas, i)
        self.max_mach = np.delete(self.max_mach, i)
        self.vs = np.delete(self.vs, i)                               
        self.fpa = np.delete(self.fpa, i)                               
        self.vertical_mode = np.delete(self.vertical_mode, i)
        self.mass = np.delete(self.mass, i)                               
        self.empty_weight = np.delete(self.empty_weight, i)
        self.fuel_weight = np.delete(self.fuel_weight, i)                     
        self.payload_weight = np.delete(self.payload_weight, i)                   
        self.fuel_consumed = np.delete(self.fuel_consumed, i)

        self.perf.del_aircraft(i)                             
        self.ap.del_aircraft(i)                               
        self.weather.del_aircraft(i)                             
    

    
    def update(self, global_time, d_t = 1):
        """
        Update aircraft state for each timestep given ATC/autopilot command.

        Parameters
        ----------
        d_t: float
            delta time per timestep [s] TODO: need?
        """

        # Update atmosphere
        self.weather.update(self.lat, self.long, self.alt, self.perf, global_time)

        # Ceiling
        # min_speed = self.perf.cal_minimum_speed(self.flight_phase)
        # max_d_tas = self.perf.cal_max_d_tas(d_t)
        # max_d_rocd = self.perf.cal_max_d_rocd(d_t, self.unit.knots_to_mps(self.d_cas), tas, self.unit.ftpm_to_mps(self.vs))

        self.speed_mode = np.where(self.alt < self.trans_alt, SpeedMode.CAS, SpeedMode.MACH)

        # Update autopilot
        self.ap.update(self)

         # Flight phase and configuration
        # Take off -> climb
        # self.flight_phase = np.where((self.flight_phase == Flight_phase.TAKEOFF) & (self.alt > 1500.0), Flight_phase.CLIMB, self.flight_phase)
        # self.flight_phase = np.where((self.flight_phase != Flight_phase.TAKEOFF) & (self.vertical_mode == Vertical_mode.CLIMB), Flight_phase.CLIMB, self.flight_phase)
        # # Climb -> Cruise
        # self.flight_phase = np.where(self.vertical_mode == Vertical_mode.LEVEL, Flight_phase.CRUISE, self.flight_phase)         #TODO: Or use cruise altitude?
        # # Cruise-Descent
        # self.flight_phase = np.where(self.vertical_mode == Vertical_mode.DESCENT, Flight_phase.DESCENT, self.flight_phase)
        self.configuration = self.perf.update_configuration(self.cas, self.alt, self.vertical_mode)
        # !TODO Is flight phase needed anymore?
        self.flight_phase = np.select(condlist=[
            (self.configuration == Config.TAKEOFF) & (self.alt > 0.0),
            self.configuration == Config.INITIAL_CLIMB,
            (self.vertical_mode == VerticalMode.CLIMB) & (self.alt < self.cruise_alt),
            self.alt == self.cruise_alt,
            (self.vertical_mode == VerticalMode.DESCENT) & (self.alt < self.cruise_alt) & (self.configuration == Config.CLEAN),
            self.configuration == Config.APPROACH,
            self.configuration == Config.LANDING,
            (self.flight_phase == FlightPhase.LANDING) & (self.alt == 0.0)
                                    ],
                                    choicelist=[
                                        FlightPhase.TAKEOFF,
                                        FlightPhase.INITIAL_CLIMB,
                                        FlightPhase.CLIMB,
                                        FlightPhase.CRUISE,
                                        FlightPhase.DESCENT,
                                        FlightPhase.APPROACH,
                                        FlightPhase.LANDING,
                                        FlightPhase.TAXI_DEST
                                    ],
                                    default=FlightPhase.CRUISE)

        # Bank angle
        d_heading = Cal.cal_angle_diff(self.heading, self.ap.heading)
        self.bank_angle = np.select(condlist=[
                                        d_heading > 0.5,
                                        d_heading < -0.5,
                                    ],
                                    choicelist=[
                                        self.perf.get_bank_angles(self.configuration),                   # Turn right
                                        np.negative(self.perf.get_bank_angles(self.configuration))       # Turn left
                                    ],
                                    default = 0.0
                                )
                                
        tas = Unit.kts2mps(self.tas)   #TAS in m/s
        self.vs, self.accel = self.perf.cal_vs_accel(self, tas)
        
        # Air Speed
        # self.tas = self.perf.cas_to_tas(self.cas, self.weather.p, self.weather.rho)
        tas = tas + self.accel
        self.mach = self.perf.tas_to_mach(tas, self.weather.T)       
        self.cas = Unit.mps2kts(self.perf.tas_to_cas(tas, self.weather.p, self.weather.rho))

        # Bound to autopilot
        self.mach = np.select(condlist=[
            (self.speed_mode == SpeedMode.MACH) & (self.ap.speed_mode == APSpeedMode.ACCELERATE),
            (self.speed_mode == SpeedMode.MACH) & (self.ap.speed_mode == APSpeedMode.DECELERATE),
            (self.speed_mode == SpeedMode.MACH) & (self.ap.speed_mode == APSpeedMode.CONSTANT_MACH)
                            ],
                            choicelist=[
                                np.where(self.mach > self.ap.mach, self.ap.mach, self.mach),
                                np.where(self.mach < self.ap.mach, self.ap.mach, self.mach),
                                self.ap.mach
                            ],
                            default=self.mach)

        self.cas = np.select(condlist=[
            (self.speed_mode == SpeedMode.CAS) & (self.ap.speed_mode == APSpeedMode.ACCELERATE),
            (self.speed_mode == SpeedMode.CAS) & (self.ap.speed_mode == APSpeedMode.DECELERATE),
            (self.speed_mode == SpeedMode.CAS) & (self.ap.speed_mode == APSpeedMode.CONSTANT_CAS)
                            ],
                            choicelist=[
                                np.where(self.cas > self.ap.cas, self.ap.cas, self.cas),    #TODO: change to minimum
                                np.where(self.cas < self.ap.cas, self.ap.cas, self.cas),
                                self.ap.cas
                            ],
                            default=self.cas)

        tas = np.select(condlist=[
            self.ap.speed_mode == APSpeedMode.CONSTANT_MACH,
            self.ap.speed_mode == APSpeedMode.CONSTANT_CAS
                        ],
                        choicelist=[
                            self.perf.mach_to_tas(self.mach, self.weather.T),
                            self.perf.cas_to_tas(Unit.kts2mps(self.cas), self.weather.p, self.weather.rho)
                        ],
                        default=tas)

        tas = np.select(condlist=[
            (self.speed_mode == SpeedMode.CAS) & ((self.ap.speed_mode == APSpeedMode.ACCELERATE) | (self.ap.speed_mode == APSpeedMode.DECELERATE)) & (self.cas == self.ap.cas),
            (self.speed_mode == SpeedMode.MACH) & ((self.ap.speed_mode == APSpeedMode.ACCELERATE) | (self.ap.speed_mode == APSpeedMode.DECELERATE)) & (self.mach == self.ap.mach)
                        ],
                        choicelist=[
                            self.perf.cas_to_tas(Unit.kts2mps(self.cas), self.weather.p, self.weather.rho),
                            self.perf.mach_to_tas(self.mach, self.weather.T)
                        ],
                        default=tas)

        self.mach = np.where((self.speed_mode == SpeedMode.CAS) & ((self.ap.speed_mode == APSpeedMode.ACCELERATE) | (self.ap.speed_mode == APSpeedMode.DECELERATE)) & (self.cas == self.ap.cas),
                             self.perf.tas_to_mach(tas, self.weather.T),
                             self.mach)
        
        self.cas = np.where((self.speed_mode == SpeedMode.MACH) & ((self.ap.speed_mode == APSpeedMode.ACCELERATE) | (self.ap.speed_mode == APSpeedMode.DECELERATE)) & (self.mach == self.ap.mach),
                            Unit.mps2kts(self.perf.tas_to_cas(tas, self.weather.p, self.weather.rho)),
                            self.cas)

        self.tas = Unit.mps2kts(tas)


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

        self.path_angle = np.rad2deg(np.arctan((self.vs/60.0)/(self.tas * 1.68781)))

        # Position
        self.lat = self.lat + self.gs_north / 216000.0
        self.long = self.long + self.gs_east / 216000.0
        self.alt = self.alt + self.vs / 60.0
        self.alt = np.select(condlist=[     #handle overshoot
            self.vertical_mode == VerticalMode.CLIMB,
            self.vertical_mode == VerticalMode.DESCENT
                            ],
                            choicelist=[
                                np.where(self.alt > self.ap.alt, self.ap.alt, self.alt),
                                np.where(self.alt < self.ap.alt, self.ap.alt, self.alt)
                            ],
                            default=self.alt)

        # Fuel        
        fuel_burn = self.perf.cal_fuel_burn(self.configuration, self.tas, self.alt) 
        self.fuel_consumed = self.fuel_consumed + fuel_burn
        self.mass = self.mass - fuel_burn