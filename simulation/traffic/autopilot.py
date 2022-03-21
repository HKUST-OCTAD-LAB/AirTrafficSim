from __future__ import annotations
from dis import dis

import numpy as np

from traffic.nav import Nav
from utils.enums import AP_speed_mode, Flight_phase, Speed_mode, Vertical_mode, AP_lateral_mode
from utils.unit import Unit_conversion
from utils.cal import Calculation

class Autopilot:
    """
    Autopilot class
    """

    def __init__(self, N=1000):
        # Target altitude
        self.alt = np.zeros([N])                                
        """Autopilot target altitude [feet]"""

        # Target orientation
        self.heading = np.zeros([N])                            
        """Autopilot target heading [deg]"""
        self.track_angle = np.zeros([N])                        
        """Autopilot target track angle [deg]"""
        self.ap_rate_of_turn = np.zeros([N])                    
        """Rate of turn [deg/s]"""

        # Target speed
        self.cas = np.zeros([N])                                
        """Autopilot target calibrated air speed [knots]"""
        self.mach = np.zeros([N])                               
        """Autopilot target Mach number [dimensionless]"""

        # Target vertical speed
        self.vs = np.zeros([N])                                 
        """Autopilot target vertical speed (feet/min)"""
        self.fpa = np.zeros([N])                                
        """Flight path angle [deg]"""

        # Target position
        self.lat = np.zeros([N])                                
        """Autopilot target latitude [deg]"""
        self.long = np.zeros([N])                               
        """Autopilot target longitude [deg]"""
        self.dist = np.zeros([N])
        """Distance to next waypoint [nm]"""

        # Flight plan
        self.flight_plan_index = np.zeros([N], dtype=int)                  
        """Index of next waypoint in flight plan array [int]"""
        self.flight_plan_name = [[0.0] for _ in range(N)]          
        """2D array to store the string of waypoints [[string]]"""
        self.flight_plan_lat = [[0.0] for _ in range(N)]           
        """2D array to store the latitude of waypoints [[deg]"""
        self.flight_plan_long = [[0.0] for _ in range(N)]          
        """2D array to store the longitude of waypoints [[deg]"""
        self.flight_plan_restriction = [[0.0] for _ in range(N)]   
        """2D array of waypoint restriction (vertical...)"""

        # Flight mode
        self.speed_mode = np.zeros([N])                         
        """Autopilot speed mode [1: constant Mach, 2: constant CAS, 3: accelerate, 4: decelerate]"""
        self.auto_throttle_mode = np.zeros([N])                 
        """Autothrottle m,ode [1: Speed, 2: Thrust]"""
        self.vertical_mode = np.zeros([N])                      
        """Autopilot vertical mode [1: alt hold, 2: vs mode, 3: flc mode (flight level change), 4. VNAV]"""
        self.lateral_mode = np.zeros([N])                       
        """Autopilot lateral mode [1: heading, 2: LNAV] ATC only use heading, LNAV -> track angle"""
        self.expedite_descent = np.zeros([N], dtype=bool)       
        """Autopilot expedite climb setting [bool]"""

        # Init nav class
        # self.nav = Nav()


    def add_aircraft(self, n, lat, long, alt, heading, cas, flight_plan=[]):
        """
        Add aircraft and init flight plan

         n : int
            Index of array.
        
        lat : float
            Starting latitude of the aircraft

        long : float
            Starting longitude of the aircraft

        alt : float
            Starting altitude of the aircraft

        heading : float
            Starting heading of the aircraft

        cas : float
            Starting calibrated air speed of the aircraft

        flight_plan : String[] (optional)
            Flight plan of an aircraft
        """
        self.alt[n] = alt
        self.heading[n] = heading
        self.cas[n] = cas
        self.lateral_mode[n] = AP_lateral_mode.HEADING

        if not flight_plan == []:
            self.flight_plan_name[n] = np.array(flight_plan)
            for i, val in enumerate(flight_plan):
                if i == 0:
                    lat_tmp, long_tmp = Nav.get_fix_coordinate(val, lat, long)
                    self.flight_plan_lat[n][0] = lat_tmp
                    self.flight_plan_long[n][0] = long_tmp
                else:
                    lat_tmp, long_tmp = Nav.get_fix_coordinate(val, self.flight_plan_lat[n][i-1], self.flight_plan_long[n][i-1])
                    self.flight_plan_lat[n].append(lat_tmp)
                    self.flight_plan_long[n].append(long_tmp)
            self.lateral_mode[n] = AP_lateral_mode.LNAV


    def update(self, traffic: Traffic):
        """
        Update the autopilot status for each timestep

        Parameters
        ----------
        traffic : Traffic
            Traffic class
        """
        # Speed mode
        self.speed_mode = np.where(traffic.speed_mode == Speed_mode.CAS, 
                            np.select([self.cas < traffic.cas, self.cas == traffic.cas, self.cas > traffic.cas],
                                      [AP_speed_mode.DECELERATE, AP_speed_mode.CONSTANT_CAS, AP_speed_mode.ACCELERATE]),
                            np.select([self.mach < traffic.mach, self.mach == traffic.mach, self.mach > traffic.mach],
                                      [AP_speed_mode.DECELERATE, AP_speed_mode.CONSTANT_MACH, AP_speed_mode.ACCELERATE]))
        # Handle change in speed mode. 
        self.mach = np.where(traffic.speed_mode == Speed_mode.CAS, traffic.perf.tas_to_mach(traffic.perf.cas_to_tas(Unit_conversion.knots_to_mps(traffic.cas), traffic.weather.p, traffic.weather.rho), traffic.weather.T), self.mach)
        self.cas = np.where(traffic.speed_mode == Speed_mode.MACH, Unit_conversion.mps_to_knots(traffic.perf.tas_to_cas(traffic.perf.mach_to_tas(traffic.mach, traffic.weather.T), traffic.weather.p, traffic.weather.rho)), self.cas)

        # Vertical mode
        traffic.vertical_mode = np.select(condlist=[
                                                self.alt > traffic.alt,
                                                self.alt == traffic.alt,
                                                self.alt < traffic.alt
                                            ],
                                            choicelist=[
                                                Vertical_mode.CLIMB,
                                                Vertical_mode.LEVEL,
                                                Vertical_mode.DESCENT
                                            ])
        
        # Waypoint, track angle, and heading
        for i, val in enumerate(self.flight_plan_index):    #TODO: optimization
            if val < len(self.flight_plan_name[i]):
                self.lat[i] = self.flight_plan_lat[i][val]
                self.long[i] = self.flight_plan_long[i][val]
            else:
                self.lateral_mode[i] = AP_lateral_mode.HEADING

        dist = Calculation.cal_great_circle_distance(traffic.lat, traffic.long, self.lat, self.long)
        self.track_angle = Calculation.cal_great_circle_bearing(traffic.lat, traffic.long, self.lat, self.long)
        self.heading = np.where(self.lateral_mode == AP_lateral_mode.HEADING, self.heading, self.track_angle + np.arcsin(traffic.weather.wind_speed/traffic.tas * np.sin(self.track_angle-traffic.weather.wind_direction))) #https://www.omnicalculator.com/physics/wind-correction-angle
        self.flight_plan_index = np.where(dist > self.dist, self.flight_plan_index+1, self.flight_plan_index)
        self.dist = dist

    def update_fms(self):
        pass
        # After transitions altitude, constant mach 
        # self.perf.get_procedure_speed(self.unit.feet_to_meter(self.alt), self.trans_alt, self.flight_phase)