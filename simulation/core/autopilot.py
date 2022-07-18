from __future__ import annotations

import numpy as np

from core.nav import Nav
from utils.cal import Calculation
from utils.enums import AP_speed_mode, AP_throttle_mode, Speed_mode, Vertical_mode, AP_lateral_mode
from utils.unit import Unit_conversion
from utils.cal import Calculation

class Autopilot:
    """
    Autopilot class
    """

    def __init__(self):
        # Target altitude
        self.alt = np.zeros([0])                                
        """Autopilot target altitude [feet]"""

        # Target orientation
        self.heading = np.zeros([0])                            
        """Autopilot target heading [deg]"""
        self.track_angle = np.zeros([0])                        
        """Autopilot target track angle [deg]"""
        self.ap_rate_of_turn = np.zeros([0])                    
        """Rate of turn [deg/s]"""

        # Target speed
        self.cas = np.zeros([0])                                
        """Autopilot target calibrated air speed [knots]"""
        self.mach = np.zeros([0])                               
        """Autopilot target Mach number [dimensionless]"""

        # Target vertical speed
        self.vs = np.zeros([0])                                 
        """Autopilot target vertical speed (feet/min)"""
        self.fpa = np.zeros([0])                                
        """Flight path angle [deg]"""

        # Target position
        self.lat = np.zeros([0])                                
        """Autopilot target latitude [deg]"""
        self.long = np.zeros([0])                               
        """Autopilot target longitude [deg]"""
        self.lat_next = np.zeros([0])                                
        """Autopilot target latitude for next waypoint [deg]"""
        self.long_next = np.zeros([0])                               
        """Autopilot target longitude for next waypoint [deg]"""
        self.hv_next_wp = np.ones([0], dtype=bool)
        """Autupilot hv next waypoint [bool]"""
        self.dist = np.zeros([0])
        """Distance to next waypoint [nm]"""

        # Flight plan
        self.flight_plan_index = np.zeros([0], dtype=int)                  
        """Index of next waypoint in flight plan array [int]"""
        self.flight_plan_name = []          
        """2D array to store the string of waypoints [[string]]"""
        self.flight_plan_lat = []           
        """2D array to store the latitude of waypoints [[deg...]]"""
        self.flight_plan_long = []          
        """2D array to store the longitude of waypoints [[deg...]]"""
        self.flight_plan_target_alt = []   
        """2D array of target altitude at each waypoint [[ft...]]"""
        self.flight_plan_target_speed = []   
        """2D array of target speed at each waypoint [[cas/mach...]]"""
        self.procedure_speed = np.zeros([0])
        """Procedural target speed from BADA"""

        # Flight mode
        self.speed_mode = np.zeros([0])                         
        """Autopilot speed mode [1: constant Mach, 2: constant CAS, 3: accelerate, 4: decelerate]"""
        self.auto_throttle_mode = np.zeros([0])                 
        """Autothrottle mode [1: Auto, 2: Speed]"""
        self.vertical_mode = np.zeros([0])                      
        """Autopilot vertical mode [1: alt hold, 2: vs mode, 3: flc mode (flight level change), 4. VNAV]"""
        self.lateral_mode = np.zeros([0])                       
        """Autopilot lateral mode [1: heading, 2: LNAV] ATC only use heading, LNAV -> track angle"""
        self.expedite_descent = np.zeros([0], dtype=bool)       
        """Autopilot expedite climb setting [bool]"""

        # Holding
        self.holding = np.zeros([0], dtype=bool)
        self.holding_round = np.zeros([0])  
        self.holding_info = []


    def add_aircraft(self, lat, long, alt, heading, cas, departure_airport, departure_runway, sid, arrival_airport, arrival_runway, star, approach, flight_plan, cruise_alt):
        """
        Add aircraft and init flight plan

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

        self.alt = np.append(self.alt, alt)                                
        self.heading = np.append(self.heading, heading)                    
        self.track_angle = np.append(self.track_angle, heading)                     
        self.ap_rate_of_turn = np.append(self.ap_rate_of_turn, 0.0)               
        self.cas = np.append(self.cas, cas)                             
        self.mach = np.append(self.mach, 0.0)                              
        self.vs = np.append(self.vs, 0.0)                              
        self.fpa = np.append(self.fpa, 0.0)                              
        self.lat = np.append(self.lat, 0.0)                                
        self.long = np.append(self.long, 0.0)                              
        self.lat_next = np.append(self.lat_next, 0.0)                              
        self.long_next = np.append(self.long_next, 0.0)                              
        self.hv_next_wp = np.append(self.hv_next_wp, False)
        self.dist = np.append(self.dist, 0.0)
        self.flight_plan_index = np.append(self.flight_plan_index, 0)               
        self.flight_plan_name.append([])     
        self.flight_plan_lat.append([])         
        self.flight_plan_long.append([])         
        self.flight_plan_target_alt.append([])  
        self.flight_plan_target_speed.append([])  
        self.procedure_speed = np.append(self.procedure_speed, 0.0)
        self.speed_mode = np.append(self.speed_mode, 0.0)                         
        self.auto_throttle_mode = np.append(self.auto_throttle_mode, AP_throttle_mode.SPEED)             
        self.vertical_mode = np.append(self.vertical_mode, 0.0)                      
        self.lateral_mode = np.append(self.lateral_mode, AP_lateral_mode.HEADING)                   
        self.expedite_descent = np.append(self.expedite_descent, False)
        self.holding = np.append(self.holding, False)  
        self.holding_round = np.append(self.holding_round, 0.0)  
        self.holding_info.append([])

        # if not flight_plan == []:
        # Add SID to flight plan
        if not sid == "":
            waypoint, alt_restriction_type, alt_restriction, speed_resctriction_type, speed_restriction = Nav.get_procedure(departure_airport, departure_runway, sid)
            # TODO: Ignored alt restriction 2, alt restriction type, and speed restriction type
            self.flight_plan_name[-1].extend(waypoint)
            self.flight_plan_target_alt[-1].extend(alt_restriction)
            self.flight_plan_target_speed[-1].extend(speed_restriction)

            self.hv_next_wp[-1] = True
            self.lateral_mode[-1] = AP_lateral_mode.LNAV
            self.auto_throttle_mode[-1] = AP_throttle_mode.AUTO

        # Add enroute flight plan
        if not flight_plan == []:
            self.flight_plan_name[-1].extend(flight_plan)
            if cruise_alt > -1:
                self.flight_plan_target_alt[-1].extend([cruise_alt for _ in flight_plan])
            self.flight_plan_target_speed[-1].extend([-1 for _ in flight_plan])

            self.hv_next_wp[-1] = True
            self.lateral_mode[-1] = AP_lateral_mode.LNAV
            self.auto_throttle_mode[-1] = AP_throttle_mode.AUTO

        # Add STAR to flight plan
        if not star == "":
            waypoint, alt_restriction_type, alt_restriction, speed_resctriction_type, speed_restriction = Nav.get_procedure(arrival_airport, arrival_runway, star)
            self.flight_plan_name[-1].extend(waypoint)
            self.flight_plan_target_alt[-1].extend(alt_restriction)
            self.flight_plan_target_speed[-1].extend(speed_restriction)

            self.hv_next_wp[-1] = True
            self.lateral_mode[-1] = AP_lateral_mode.LNAV
            self.auto_throttle_mode[-1] = AP_throttle_mode.AUTO

        if not approach == "":
            # Add Initial Approach to flight plan
            waypoint, alt_restriction_type, alt_restriction, speed_resctriction_type, speed_restriction = Nav.get_procedure(arrival_airport, arrival_runway, approach, appch="A", iaf=self.flight_plan_name[-1][-1])
            # Remove last element of flight plan which should be equal to iaf
            self.flight_plan_name[-1].pop()
            self.flight_plan_target_alt[-1].pop()
            self.flight_plan_target_speed[-1].pop()
            # Add Initial Approach flight plan 
            self.flight_plan_name[-1].extend(waypoint)
            self.flight_plan_target_alt[-1].extend(alt_restriction)
            self.flight_plan_target_speed[-1].extend(speed_restriction)

            # Add Final Approach to flight plan
            waypoint, alt_restriction_type, alt_restriction, speed_resctriction_type, speed_restriction = Nav.get_procedure(arrival_airport, arrival_runway, approach, appch="I")
            # Remove last element of flight plan which should be equal to iaf
            self.flight_plan_name[-1].pop()
            self.flight_plan_target_alt[-1].pop()
            self.flight_plan_target_speed[-1].pop()
            # Add Final Approach flight plan with missed approach removed)
            # waypoint_idx = waypoint.index(' ')
            # self.flight_plan_name[-1].extend(waypoint[:waypoint_idx])
            # self.flight_plan_target_alt[-1].extend(alt_restriction_1[:waypoint_idx])
            # self.flight_plan_target_speed[-1].extend(speed_restriction[:waypoint_idx])
            self.flight_plan_name[-1].extend(waypoint)
            self.flight_plan_target_alt[-1].extend(alt_restriction)
            self.flight_plan_target_speed[-1].extend(speed_restriction)
            # TODO: For missed approach procedure [waypoint_idx+1:]

            self.hv_next_wp[-1] = True
            self.lateral_mode[-1] = AP_lateral_mode.LNAV
            self.auto_throttle_mode[-1] = AP_throttle_mode.AUTO

        # Get Lat Long of flight plan waypoints
        for i, val in enumerate(self.flight_plan_name[-1]):
            if i == 0:
                lat_tmp, long_tmp = Nav.get_fix_coordinate(val, lat, long)
                self.flight_plan_lat[-1].append(lat_tmp)
                self.flight_plan_long[-1].append(long_tmp)
            else:
                lat_tmp, long_tmp = Nav.get_fix_coordinate(val, self.flight_plan_lat[-1][i-1], self.flight_plan_long[-1][i-1])
                self.flight_plan_lat[-1].append(lat_tmp)
                self.flight_plan_long[-1].append(long_tmp)

        # TODO: Add runway lat long alt
        if not arrival_runway == "":
            lat_tmp, long_tmp, alt_tmp = Nav.get_runway_coordinate(arrival_airport, arrival_runway)
            if self.flight_plan_name[-1][-1] == arrival_runway:
                self.flight_plan_lat[-1][-1] = lat_tmp
                self.flight_plan_long[-1][-1] = long_tmp
                self.flight_plan_target_alt[-1][-1] = alt_tmp
            else:
                self.flight_plan_lat[-1].append(lat_tmp)
                self.flight_plan_long[-1].append(long_tmp)
                self.flight_plan_target_alt[-1].append(alt_tmp)
                # self.flight_plan_target_speed[n]

        # Populate alt and speed target from last waypoint
        if len(self.flight_plan_target_alt[-1]) > 1:
            self.flight_plan_target_alt[-1][-1] = 0.0
            for i, val in reversed(list(enumerate(self.flight_plan_target_alt[-1]))):
                if val == -1:
                    self.flight_plan_target_alt[-1][i] = self.flight_plan_target_alt[-1][i+1]

        # for i, val in reversed(list(enumerate(self.flight_plan_target_speed[n]))):
        #     if val == -1:
        #         self.flight_plan_target_speed[n][i] = self.flight_plan_target_speed[n][i+1]

            


    def del_aircraft(self, index):
        self.alt = np.delete(self.alt, index)                                
        self.heading = np.delete(self.heading, index)                    
        self.track_angle = np.delete(self.track_angle, index)                     
        self.ap_rate_of_turn = np.delete(self.ap_rate_of_turn, index)               
        self.cas = np.delete(self.cas, index)                             
        self.mach = np.delete(self.mach, index)                              
        self.vs = np.delete(self.vs, index)                              
        self.fpa = np.delete(self.fpa, index)                              
        self.lat = np.delete(self.lat, index)                                
        self.long = np.delete(self.long, index)                              
        self.lat_next = np.delete(self.lat_next, index)                              
        self.long_next = np.delete(self.long_next, index)                              
        self.hv_next_wp = np.delete(self.hv_next_wp, index)
        self.dist = np.delete(self.dist, index)
        self.flight_plan_index = np.delete(self.flight_plan_index, index)               
        del self.flight_plan_name[index]          
        del self.flight_plan_lat[index]           
        del self.flight_plan_long[index]          
        del self.flight_plan_target_alt[index]   
        del self.flight_plan_target_speed[index]   
        self.procedure_speed = np.delete(self.procedure_speed, index)
        self.speed_mode = np.delete(self.speed_mode, index)                         
        self.auto_throttle_mode = np.delete(self.auto_throttle_mode, index)             
        self.vertical_mode = np.delete(self.vertical_mode, index)                      
        self.lateral_mode = np.delete(self.lateral_mode, index)                   
        self.expedite_descent =np.delete(self.expedite_descent, index)
        self.holding = np.delete(self.holding, index) 
        self.holding_round = np.delete(self.holding_round, index)  
        del self.holding_info[index]


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

        # self.alt = np.minimum(self.alt, traffic.max_alt)   #Altitude
        
        # Procedural speed. Follow procedural speed by default.
        # After transitions altitude, constant mach 
        self.procedure_speed = traffic.perf.get_procedure_speed(traffic.alt, traffic.trans_alt, traffic.configuration)
        # TODO: Check procedure speed with SID STAR limitation

        self.cas = np.where((self.auto_throttle_mode == AP_throttle_mode.AUTO) & (self.procedure_speed >= 5.0), self.procedure_speed, self.cas)      #TODO: Add speed mode atc
        self.cas = np.minimum(self.cas, traffic.max_cas)
        self.mach = np.where((self.auto_throttle_mode == AP_throttle_mode.AUTO) & (self.procedure_speed < 5.0), self.procedure_speed, self.mach)      #TODO: Add speed mode atc
        self.mach = np.minimum(self.mach, traffic.max_mach)

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
        # dist = np.where(self.lateral_mode == AP_lateral_mode.HEADING, 0.0, Calculation.cal_great_circle_distance(traffic.lat, traffic.long, self.lat, self.long))   #km
        dist = Calculation.cal_great_circle_distance(traffic.lat, traffic.long, self.lat, self.long)   #km

        # Fly by turn
        turn_radius = traffic.perf.cal_turn_radius(traffic.perf.get_bank_angles(traffic.configuration), Unit_conversion.knots_to_mps(traffic.tas)) / 1000.0     #km
        next_track_angle = np.where(self.hv_next_wp, Calculation.cal_great_circle_bearing(self.lat, self.long, self.lat_next, self.long_next), self.track_angle)    # Next track angle to next next waypoint
        curr_track_angle = Calculation.cal_great_circle_bearing(traffic.lat, traffic.long, self.lat, self.long) # Current track angle to next waypoint
        turn_dist = turn_radius * np.tan(np.deg2rad(np.abs(Calculation.cal_angle_diff(next_track_angle, curr_track_angle))/2.0))    # Distance to turn
        self.track_angle =  np.where(self.lateral_mode == AP_lateral_mode.HEADING, 0.0, np.where(dist < turn_dist, np.where(self.hv_next_wp, next_track_angle, self.track_angle), np.where(dist < 1.0, self.track_angle, curr_track_angle)))       
        self.heading = np.where(self.lateral_mode == AP_lateral_mode.HEADING, self.heading, self.track_angle + np.arcsin(traffic.weather.wind_speed/traffic.tas * np.sin(self.track_angle-traffic.weather.wind_direction))) #https://www.omnicalculator.com/physics/wind-correction-angle
        
        update_next_wp = (self.lateral_mode == AP_lateral_mode.LNAV) & (dist > self.dist) & (np.abs(Calculation.cal_angle_diff(traffic.heading, next_track_angle)) < 1.0)
        self.flight_plan_index = np.where(update_next_wp, self.flight_plan_index+1, self.flight_plan_index)
        self.dist = np.where(update_next_wp, Calculation.cal_great_circle_distance(traffic.lat, traffic.long, self.lat_next, self.long_next), dist)

        # Fly over turn
        # self.track_angle =  np.where(self.lateral_mode == AP_lateral_mode.HEADING, 0.0, np.where(dist<1.0, self.track_angle, Calculation.cal_great_circle_bearing(traffic.lat, traffic.long, self.lat, self.long)))
        # self.heading = np.where(self.lateral_mode == AP_lateral_mode.HEADING, self.heading, self.track_angle + np.arcsin(traffic.weather.wind_speed/traffic.tas * np.sin(self.track_angle-traffic.weather.wind_direction))) #https://www.omnicalculator.com/physics/wind-correction-angle
        # self.flight_plan_index = np.where((self.lateral_mode == AP_lateral_mode.LNAV) & (dist < 1.0) & (dist > self.dist), self.flight_plan_index+1, self.flight_plan_index)
        # self.dist = dist

        # Holding
        for i, val in enumerate(self.holding):
            if self.holding[i] == False:
                if self.holding_info[i] and np.abs(Calculation.cal_angle_diff(self.heading[i], self.holding_info[i][4])) < 90.0 and self.flight_plan_index[i] > self.flight_plan_name[i].index(self.holding_info[i][0]):   # Turn outbound
                    self.heading[i] = np.mod(self.holding_info[i][4] + 180, 360)
                    self.holding_round[i] -= 1
                    self.flight_plan_index[i] -= 1
                    self.lateral_mode[i] = AP_lateral_mode.HEADING
                    self.holding[i] = True        
            else:
                if np.abs(Calculation.cal_angle_diff(self.heading[i], self.holding_info[i][4])) < 90.0 and dist[i] < 1:   # Turn outbound
                    self.heading[i] = np.mod(self.holding_info[i][4] + 180, 360)
                    self.holding_round[i] -= 1

                if np.abs(Calculation.cal_angle_diff(self.heading[i], self.holding_info[i][4] + 180.0)) < 90.0 and dist[i] > Unit_conversion.nm_to_meter(self.holding_info[i][6])/1000.0: # Turn inbound
                    self.heading[i] = self.holding_info[i][4]
                    if self.holding_round[i] <= 0:
                        self.lateral_mode[i] = AP_lateral_mode.LNAV
                        self.holding[i] = False
                        self.holding_info[i] = []
                
                    # update_next_wp[i] = False
        
        