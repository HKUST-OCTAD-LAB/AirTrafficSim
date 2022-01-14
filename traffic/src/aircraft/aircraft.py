import numpy as np

class Aircraft:

    def __init__(self, lat, long, heading, tas):
        """
        Initialize aircrafts state variables for one timestep.

        Parameters
        ----------
        
        """

        # General information
        # self.call_sign = "1"              # Callsign [string]
        # self.aircraft_type = aircraft_type          # Aircraft type in ICAO format [string]
        # self.flight_phase = 1                      # Flight phase [At gate:1, Taxi: 2, Takeoff: 3, Climb: 4, Cruise: 5, Descent: 6, Approach: 7, Landing: 8, Taxi: 9, At Gate: 10]

        # Position
        self.long = long                   # Longitude [deg]
        self.lat = lat                    # Latitude [deg]
        # self.alt = alt                    # Altitude [ft/m] TODO: define altitude unit

        # Orientation
        self.heading = heading                  # Heading [deg]
        # self.track_angle = np.zeros([N])            # Track angle [deg]
        self.bank_angle = 0             # Bank angle [deg]

        # Speed
        # self.ias = np.zeros([N])                    # Indicated air speed [knot]
        # self.cas = np.zeros([N])                    # Calibrated air speed [knot]
        self.tas = tas                   # True air speed [knot]
        self.gs_north = 0                       # Ground speed [knot]
        self.gs_east = 0                        # Ground speed [knot]  
        # self.mach = np.zeros([N])                   # Mach number [dimensionless]
        # self.vs = np.zeros([N])                     # Vertical speed [ft/min]

        # Weight and balance
        # self.weight = np.zeros([N])                 # Aircraft weight [kg]
        # self.fuel_weight = np.zeros([N])            # Fuel weight [kg]
        # self.payload_weight = np.zeros([N])         # Payload weight [kg]

        # # Autopilot
        # self.ap_heading = heading                     # Autopilot heading
        # self.ap_rate_of_turn = 0           # Rate of turn [deg/s]

        # Constant
        self.__g_0 = 9.80665                # Gravitational acceleration [m/s^2]


    def __convert_tas_to_mps(tas):
        # Convert True air speed to meter per second (1nm = 1852m, 1 hr = 3600s)
        return tas * 1852 / 3600

    def update(self, ap_heading, wind_north = 0, wind_east = 0):
        """
        Update aircraft state for each timestep.
        """

        # Turn
        print("Set heading:", ap_heading)
        if(ap_heading - self.heading > 3):
            self.heading += 3
        elif(ap_heading - self.heading < -3):
            self.heading -= 3
        else:
            self.heading = ap_heading

        if (self.heading > 360):
            self.heading = self.heading - 360
        if (self.heading < 0):
            self.heading = 360 + self.heading

        # self.ap_rate_of_turn = rate_of_turn
        print("Current heading:", self.heading)

        # Calculate ground speed
        self.gs_north = self.tas * np.cos(np.deg2rad(self.heading)) + wind_north
        self.gs_east = self.tas * np.sin(np.deg2rad(self.heading)) + wind_east
        print("Ground speed: (North/East)", self.gs_north, self.gs_east)

        # Calculate position
        self.lat = self.lat + self.gs_north / 216000
        self.long = self.long + self.gs_east / 216000
        print("Position: ", self.lat, self.long)


    
