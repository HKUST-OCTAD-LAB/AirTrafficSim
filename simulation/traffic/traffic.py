import numpy as np

from simulation.traffic.autopilot import Autopilot
from simulation.traffic.weather import Weather
from simulation.traffic.performance import Performance

class Traffic:

    def __init__(self, N=1000):
        """
        Initialize base traffic array to store aircraft state variables for one timestep.
        """

        # Memory and index control vairable:
        self.n = 0                                              # Aircraft count
        self.N = N                                              # Maximum aircraft count
        self.index = np.zeros([N])                              # Index array to indicate whether there is an aircraft active in each index.

        # General information
        self.call_sign = np.empty([N], dtype='U10')             # Callsign [string]
        self.aircraft_type = np.empty([N], dtype='U4')          # Aircraft type in ICAO format [string]
        self.flight_phase = np.zeros([N])                       # Flight phase [Flight_phase enum] (BADA section 3.5)

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
            n= self.n

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
        self.n += 1

        return self.n-1


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