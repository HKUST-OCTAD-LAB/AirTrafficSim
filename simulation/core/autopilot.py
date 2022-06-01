from __future__ import annotations

import numpy as np

from core.nav import Nav
from utils.enums import AP_speed_mode, Speed_mode, Vertical_mode, AP_lateral_mode
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
        self.lat_next = np.zeros([N])                                
        """Autopilot target latitude for next waypoint [deg]"""
        self.long_next = np.zeros([N])                               
        """Autopilot target longitude for next waypoint [deg]"""
        self.hv_next_wp = np.ones([N], dtype=bool)
        """Autupilot hv next waypoint [bool]"""
        self.dist = np.zeros([N])
        """Distance to next waypoint [nm]"""

        # Flight plan
        self.flight_plan_index = np.zeros([N], dtype=int)                  
        """Index of next waypoint in flight plan array [int]"""
        self.flight_plan_name = [[] for _ in range(N)]          
        """2D array to store the string of waypoints [[string]]"""
        self.flight_plan_lat = [[] for _ in range(N)]           
        """2D array to store the latitude of waypoints [[deg...]]"""
        self.flight_plan_long = [[] for _ in range(N)]          
        """2D array to store the longitude of waypoints [[deg...]]"""
        self.flight_plan_target_alt = [[] for _ in range(N)]   
        """2D array of target altitude at each waypoint [[ft...]]"""
        self.flight_plan_target_speed = [[] for _ in range(N)]   
        """2D array of target speed at each waypoint [[cas/mach...]]"""
        self.procedure_speed = np.zeros([N])
        """Procedural target speed from BADA"""

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


    def add_aircraft(self, n, lat, long, alt, heading, cas, departure_airport, departure_runway, sid, arrival_airport, arrival_runway, star, approach, flight_plan, cruise_alt):
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
            # Add SID to flight plan
            if not sid == "":
                waypoint, alt_restriction_type, alt_restriction_1, alt_restriction_2, speed_resctriction_type, speed_restriction = Nav.get_procedure(departure_airport, departure_runway, sid)
                # TODO: Ignored alt restriction 2, alt restriction type, and speed restriction type
                self.flight_plan_name[n].extend(waypoint)
                self.flight_plan_target_alt[n].extend(alt_restriction_1)
                self.flight_plan_target_speed[n].extend(speed_restriction)

            # Add enroute flight plan
            self.flight_plan_name[n].extend(flight_plan)
            self.flight_plan_target_alt[n].extend([cruise_alt for _ in flight_plan])
            self.flight_plan_target_speed[n].extend([-1 for _ in flight_plan])

            # Add STAR to flight plan
            if not star == "":
                waypoint, alt_restriction_type, alt_restriction_1, alt_restriction_2, speed_resctriction_type, speed_restriction = Nav.get_procedure(arrival_airport, arrival_runway, star)
                self.flight_plan_name[n].extend(waypoint)
                self.flight_plan_target_alt[n].extend(alt_restriction_1)
                self.flight_plan_target_speed[n].extend(speed_restriction)

            if not approach == "":
                # Add Initial Approach to flight plan
                waypoint, alt_restriction_type, alt_restriction_1, alt_restriction_2, speed_resctriction_type, speed_restriction = Nav.get_procedure(arrival_airport, arrival_runway, approach, appch="A", iaf=self.flight_plan_name[n][-1])
                # Remove last element of flight plan which should be equal to iaf
                self.flight_plan_name[n].pop()
                self.flight_plan_target_alt[n].pop()
                self.flight_plan_target_speed[n].pop()
                # Add Initial Approach flight plan 
                self.flight_plan_name[n].extend(waypoint)
                self.flight_plan_target_alt[n].extend(alt_restriction_1)
                self.flight_plan_target_speed[n].extend(speed_restriction)

                # Add Final Approach to flight plan
                waypoint, alt_restriction_type, alt_restriction_1, alt_restriction_2, speed_resctriction_type, speed_restriction = Nav.get_procedure(arrival_airport, arrival_runway, approach, appch="I")
                # Remove last element of flight plan which should be equal to iaf
                self.flight_plan_name[n].pop()
                self.flight_plan_target_alt[n].pop()
                self.flight_plan_target_speed[n].pop()
                # Add Final Approach flight plan with missed approach removed)
                waypoint_idx = waypoint.index(' ')
                self.flight_plan_name[n].extend(waypoint[:waypoint_idx])
                self.flight_plan_target_alt[n].extend(alt_restriction_1[:waypoint_idx])
                self.flight_plan_target_speed[n].extend(speed_restriction[:waypoint_idx])
                # TODO: For missed approach procedure [waypoint_idx+1:]

            # Get Lat Long of flight plan waypoints
            for i, val in enumerate(self.flight_plan_name[n]):
                if i == 0:
                    lat_tmp, long_tmp = Nav.get_fix_coordinate(val, lat, long)
                    self.flight_plan_lat[n].append(lat_tmp)
                    self.flight_plan_long[n].append(long_tmp)
                else:
                    lat_tmp, long_tmp = Nav.get_fix_coordinate(val, self.flight_plan_lat[n][i-1], self.flight_plan_long[n][i-1])
                    self.flight_plan_lat[n].append(lat_tmp)
                    self.flight_plan_long[n].append(long_tmp)

            # TODO: Add runway lat long alt
            lat_tmp, long_tmp, alt_tmp = Nav.get_runway_coordinate(arrival_airport, arrival_runway)
            if self.flight_plan_name[n][-1] == arrival_runway:
                self.flight_plan_lat[n][-1] = lat_tmp
                self.flight_plan_long[n][-1] = long_tmp
                self.flight_plan_target_alt[n][-1] = alt_tmp
            else:
                self.flight_plan_lat[n].append(lat_tmp)
                self.flight_plan_long[n].append(long_tmp)
                self.flight_plan_target_alt[n].append(alt_tmp)
                # self.flight_plan_target_speed[n]
            

            # Populate alt and speed target from last waypoint
            self.flight_plan_target_alt[n][-1] = 0.0
            for i, val in reversed(list(enumerate(self.flight_plan_target_alt[n]))):
                if val == -1:
                    self.flight_plan_target_alt[n][i] = self.flight_plan_target_alt[n][i+1]

            # for i, val in reversed(list(enumerate(self.flight_plan_target_speed[n]))):
            #     if val == -1:
            #         self.flight_plan_target_speed[n][i] = self.flight_plan_target_speed[n][i+1]

            self.lateral_mode[n] = AP_lateral_mode.LNAV


    def update(self, traffic: Traffic):
        """
        Update the autopilot status for each timestep

        Parameters
        ----------
        traffic : Traffic
            Traffic class
        """
        # Update target based on flight plan
        for i, val in enumerate(self.flight_plan_index):    #TODO: optimization
            if val < len(self.flight_plan_name[i]):
                # Target Flight Plan Lat/Long
                self.lat[i] = self.flight_plan_lat[i][val]
                self.long[i] = self.flight_plan_long[i][val]
                if val == len(self.flight_plan_name[i]) - 1 :
                    self.hv_next_wp[i] = False
                else :
                    self.lat_next[i] = self.flight_plan_lat[i][val+1]
                    self.long_next[i] = self.flight_plan_long[i][val+1]
                    self.hv_next_wp[i] = True
                    
                # Target Flight Plan Altitude
                if len(self.flight_plan_target_alt[i]) > 1:
                    self.alt[i] = self.flight_plan_target_alt[i][val]
                # Target Flight Plan Speed
                # if len(self.flight_plan_target_speed[i]) > 1:
                #     if (self.flight_plan_target_speed[i][val] < 1.0):
                #         self.mach[i] = self.flight_plan_target_speed[i][val]
                #     else:
                #         self.cas[i] = self.flight_plan_target_speed[i][val]
            else:
                self.lateral_mode[i] = AP_lateral_mode.HEADING
        
        # Procedural speed. Follow procedural speed by default.
        # After transitions altitude, constant mach 
        self.procedure_speed = traffic.perf.get_procedure_speed(traffic.alt, traffic.trans_alt, traffic.configuration)
        # TODO: Check procedure speed with SID STAR limitation

        self.cas = np.where(self.procedure_speed >= 5.0, self.procedure_speed, self.cas)      #TODO: Add speed mode atc
        self.mach = np.where(self.procedure_speed < 5.0, self.procedure_speed, self.mach)      #TODO: Add speed mode atc

        # Handle change in speed mode. 
        self.mach = np.where(traffic.speed_mode == Speed_mode.CAS, traffic.perf.tas_to_mach(traffic.perf.cas_to_tas(Unit_conversion.knots_to_mps(self.cas), traffic.weather.p, traffic.weather.rho), traffic.weather.T), self.mach)
        self.cas = np.where(traffic.speed_mode == Speed_mode.MACH, Unit_conversion.mps_to_knots(traffic.perf.tas_to_cas(traffic.perf.mach_to_tas(self.mach, traffic.weather.T), traffic.weather.p, traffic.weather.rho)), self.cas)

        # Speed mode
        self.speed_mode = np.where(traffic.speed_mode == Speed_mode.CAS, 
                            np.select([self.cas < traffic.cas, self.cas == traffic.cas, self.cas > traffic.cas],
                                      [AP_speed_mode.DECELERATE, AP_speed_mode.CONSTANT_CAS, AP_speed_mode.ACCELERATE]),
                            np.select([self.mach < traffic.mach, self.mach == traffic.mach, self.mach > traffic.mach],
                                      [AP_speed_mode.DECELERATE, AP_speed_mode.CONSTANT_MACH, AP_speed_mode.ACCELERATE]))

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
        dist = np.where(self.lateral_mode == AP_lateral_mode.HEADING, 0.0, Calculation.cal_great_circle_distance(traffic.lat, traffic.long, self.lat, self.long))   #km

        # Fly by turn
        turn_radius = traffic.perf.cal_turn_radius(traffic.perf.get_bank_angles(traffic.configuration), Unit_conversion.knots_to_mps(traffic.tas)) / 1000.0     #km
        next_track_angle = np.where(self.hv_next_wp, Calculation.cal_great_circle_bearing(self.lat, self.long, self.lat_next, self.long_next), self.track_angle)    # Next track angle to next next waypoint
        curr_track_angle = Calculation.cal_great_circle_bearing(traffic.lat, traffic.long, self.lat, self.long) # Current track angle to next waypoint
        turn_dist = turn_radius * np.tan(np.deg2rad(np.abs(Calculation.cal_angle_diff(next_track_angle, curr_track_angle))/2.0))    # Distance to turn
        self.track_angle =  np.where(self.lateral_mode == AP_lateral_mode.HEADING, 0.0, np.where(dist < turn_dist, np.where(self.hv_next_wp, next_track_angle, self.track_angle), np.where(dist < 1.0, self.track_angle, curr_track_angle)))
        self.heading = np.where(self.lateral_mode == AP_lateral_mode.HEADING, self.heading, self.track_angle + np.arcsin(traffic.weather.wind_speed/traffic.tas * np.sin(self.track_angle-traffic.weather.wind_direction))) #https://www.omnicalculator.com/physics/wind-correction-angle
        
        update_next_wp = (self.lateral_mode == AP_lateral_mode.LNAV) & (dist > self.dist) & (np.abs(Calculation.cal_angle_diff(traffic.heading, next_track_angle)) < 1.0)
        self.flight_plan_index = np.where(update_next_wp, self.flight_plan_index+1, self.flight_plan_index)
        self.dist = np.where(update_next_wp, Calculation.cal_great_circle_distance(traffic.lat, traffic.long, self.lat_next, self.long_next),dist)

        # Fly over turn
        # self.track_angle =  np.where(self.lateral_mode == AP_lateral_mode.HEADING, 0.0, np.where(dist<1.0, self.track_angle, Calculation.cal_great_circle_bearing(traffic.lat, traffic.long, self.lat, self.long)))
        # self.heading = np.where(self.lateral_mode == AP_lateral_mode.HEADING, self.heading, self.track_angle + np.arcsin(traffic.weather.wind_speed/traffic.tas * np.sin(self.track_angle-traffic.weather.wind_direction))) #https://www.omnicalculator.com/physics/wind-correction-angle
        # self.flight_plan_index = np.where((self.lateral_mode == AP_lateral_mode.LNAV) & (dist < 1.0) & (dist > self.dist), self.flight_plan_index+1, self.flight_plan_index)
        # self.dist = dist
        
        