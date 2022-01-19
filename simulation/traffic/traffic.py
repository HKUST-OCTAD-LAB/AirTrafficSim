import numpy as np

from .autopilot import Autopilot
from .weather import Weather
from .performance import Performance

class Traffic:

    def __init__(self, N=1000):
        """
        Initialize base traffic array to store aircraft state variables for one timestep.
        """

        # State vairable:
        self.n = 0                                              # Aircraft cont

        # General information
        self.call_sign = np.empty([N], dtype='U10')             # Callsign [string]
        self.aircraft_type = np.empty([N], dtype='U4')          # Aircraft type in ICAO format [string]
        self.flight_phase = np.zeros([N])                       # Flight phase [1: At gate, 2: Taxi, 3: Takeoff, 4: Climb, 5: Cruise, 6: Descent, 7: Approach, 8: Landing, 9: Taxi, 10: At Gate]

        # Position
        self.lat = np.zeros([N])                                # Latitude [deg]
        self.long = np.zeros([N])                               # Longitude [deg]
        self.alt = np.zeros([N])                                # Altitude [ft]

        # Orientation
        self.heading = np.zeros([N])                            # Heading [deg]
        self.track_angle = np.zeros([N])                        # Track angle [deg]
        self.bank_angle = np.zeros([N])                         # Bank angle [deg]

        # Speed
        self.ias = np.zeros([N])                                # Indicated air speed [knot]
        self.cas = np.zeros([N])                                # Calibrated air speed [knot]
        self.tas = np.zeros([N])                                # True air speed [knot]
        self.gs_north = np.zeros([N])                           # Ground speed - North[knot]
        self.gs_east = np.zeros([N])                            # Ground speed - East [knot]  
        self.mach = np.zeros([N])                               # Mach number [dimensionless]

        # Vertical speed
        self.vs = np.zeros([N])                                 # Vertical speed [feet/min]
        self.fpa = np.zeros([N])                                # Flight path angle [deg]

        # Weight and balance
        self.weight = np.zeros([N])                             # Aircraft weight [kg]
        self.fuel_weight = np.zeros([N])                        # Fuel weight [kg]
        self.payload_weight = np.zeros([N])                     # Payload weight [kg]

        # "Sub" classes
        self.perf = Performance(N)                              # Performance class
        self.ap = Autopilot(N)                                  # Autopilot class
        self.weather = Weather(N)                               # Weather class

    
    def add_aircraft(self, call_sign, aircraft_type, flight_phase, lat, long, alt, heading, tas, weight, fuel_weight, payload_weight):
        """
        Add an aircraft to traffic array.

        Returns
        -------
        self.n-1: int
            Index of the added aircraft
        """

        print("Traffic.py - add_aircraft()", call_sign, " Type:",  aircraft_type)

        # Initialize variables
        self.call_sign[self.n] = call_sign
        self.aircraft_type[self.n] = aircraft_type
        self.flight_phase[self.n] = flight_phase
        self.lat[self.n] = lat
        self.long[self.n] = long
        self.alt[self.n] = alt
        self.heading[self.n] = heading
        self.tas[self.n] = tas
        self.weight[self.n] = weight
        self.fuel_weight[self.n] = fuel_weight
        self.payload_weight[self.n] = payload_weight

        # Add aircraft in performance array
        self.perf.add_aircraft(aircraft_type, self.n)
        
        # Increase aircraft count
        self.n += 1

        return self.n-1


    def remove_aircraft(self):
        """
        Remove an aircraft from traffic array.
        TODO:
        """
        pass
    

    
    def update(self, i = -1):
        """
        Update aircraft state for each timestep.

        Parameters
        ----------
        i: int
            Index of the specific aircraft to undergo calculation. If undefined, update will calculate all aircraft
        """

        print("Traffic.py - update()")

        if (i == -1):
            i = 0
            n = self.n      # Set number of aircraft to be total number
        else:
            n = i + 1
        
        # Turn (assume standard 3 deg/s turn)
        print("Set heading:", self.ap.heading[i:n])

        if(self.ap.heading[i:n] - self.heading[i:n] > 3):
            self.heading[i:n] += 3
        elif(self.ap.heading[i:n] - self.heading[i:n] < -3):
            self.heading[i:n] -= 3
        else:
            self.heading[i:n] = self.ap.heading[i:n]

        if (self.heading[i:n] > 360):
            self.heading[i:n] = self.heading[i:n] - 360
        if (self.heading[i:n] < 0):
            self.heading[i:n] = 360 + self.heading[i:n]

        # self.ap_rate_of_turn = rate_of_turn
        print("Current heading:", self.heading[i:n])

        # Calculate ground speed
        self.gs_north[i:n] = self.tas[i:n] * np.cos(np.deg2rad(self.heading[i:n])) + self.weather.wind_north[i:n]
        self.gs_east[i:n] = self.tas[i:n] * np.sin(np.deg2rad(self.heading[i:n])) + self.weather.wind_east[i:n]
        print("Ground speed: (North/East)", self.gs_north[i:n], self.gs_east[i:n])

        # Calculate position
        self.lat[i:n] = self.lat[i:n] + self.gs_north[i:n] / 216000
        self.long[i:n] = self.long[i:n] + self.gs_east[i:n] / 216000
        print("Position: ", self.lat[i:n], self.long[i:n])