from turtle import speed
import numpy as np

from utils.enums import AP_speed_mode, Flight_phase, Traffic_speed_mode

class Autopilot:
    """
    Calculate target state
    """

    def __init__(self, N=1000):
        # Target position
        self.lat = np.zeros([N])                                # Autopilot target latitude [deg]
        self.long = np.zeros([N])                               # Autopilot target longitude [deg]
        self.alt = np.zeros([N])                                # Autopilot target altitude [feet]

        # Target orientation
        self.heading = np.zeros([N])                            # Autopilot target heading [deg]
        self.track_angle = np.zeros([N])                        # Autopilot target track angle [deg]
        self.ap_rate_of_turn = np.zeros([N])                    # Rate of turn [deg/s]

        # Target speed
        self.cas = np.zeros([N])                                # Autopilot target calibrated air speed [knots]
        self.mach = np.zeros([N])                               # Autopilot target Mach number [dimensionless]

        # Target vertical speed
        self.vs = np.zeros([N])                                 # Autopilot target vertical speed (feet/min)
        self.fpa = np.zeros([N])                                # Flight path angle [deg]

        # Flight plan
        self.flight_plan_name = [[]]                            # Python 2D list to store the string of waypoints [[string]
        self.flight_plan_lat = [[]]                             # Python 2D list to store the latitude of waypoints [[deg]
        self.flight_plan_long = [[]]                            # Python 2D list to store the longitude of waypoints [[deg]
        self.waypoint_index = np.zeros([N])                     # Index of target waypoint [int]
        self.waypoint_restriction = [[]]                        # Python 2D list of waypoint restriction (vertical...) TODO:
        self.waypoint_lat = np.zeros([N])                       # Latitude of target waypoint [deg]
        self.waypoint_long = np.zeros([N])                      # Longitude of target waypoint [deg]

        # Flight mode
        self.speed_mode = np.zeros([N])                         # Autopilot speed mode [1: constant Mach, 2: constant CAS, 3: accelerate, 4: decelerate]
        self.auto_throttle_mode = np.zeros([N])                 # Autothrottle m,ode [1: Speed, 2: Thrust]
        self.vertical_mode = np.zeros([N])                      # Autopilot vertical mode [1: alt hold, 2: vs mode, 3: flc mode (flight level change), 4. VNAV]
        self.lateral_mode = np.zeros([N])                       # Autopilot lateral mode [1: heading, 2: track angle, 3: LNAV] ATC only use heading, LNAV -> track angle
        self.expedite_descent = np.zeros([N], dtype=bool)       # Autopilot expedite climb setting [bool]


    def update(self, speed_mode, cas, mach, alt, flight_phase):
        self.speed_mode = np.where(speed_mode == Traffic_speed_mode.CAS, 
                            np.select([self.cas < cas, self.cas == cas, self.cas > cas],
                                      [AP_speed_mode.DECELERATE, AP_speed_mode.CONSTANT_CAS, AP_speed_mode.ACCELERATE]),
                            np.select([self.mach < mach, self.mach == mach, self.mach > mach],
                                      [AP_speed_mode.DECELERATE, AP_speed_mode.CONSTANT_MACH, AP_speed_mode.ACCELERATE]))

        flight_phase = np.select(condlist=[
                                    self.alt > alt,
                                    self.alt == alt,
                                    self.alt < alt
                                ],
                                choicelist=[
                                    Flight_phase.CLIMB,
                                    Flight_phase.CRUISE,
                                    Flight_phase.DESCENT
                                ])
        

    def update_fms(self):
        pass
        # After transitions altitude, constant mach 
        # self.perf.get_procedure_speed(self.unit.feet_to_meter(self.alt), self.trans_alt, self.flight_phase)