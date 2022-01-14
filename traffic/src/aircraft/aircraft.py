import numpy as np

class Aircraft:

    def __init__(self, N=1000):
        """
        Initialize aircrafts state variables for one timestep.

        Parameters
        ----------
        N: int
            Number of aircrafts. Maximum size of aircrafts array (pre-initialize to to eliminate inefficient append)
        """

        # General information
        self.call_sign = np.empty([N])              # Callsign [string]
        self.aircraft_type = np.empty([N])          # Aircraft type in ICAO format [string]
        self.flight_phase = np.zeros([N])           # Flight phase [At gate:1, Taxi: 2, Takeoff: 3, Climb: 4, Cruise: 5, Descent: 6, Approach: 7, Landing: 8, Taxi: 9, At Gate: 10]

        # Position
        self.long = np.zeros([N])                   # Longitude [deg]
        self.lat = np.zeros([N])                    # Latitude [deg]
        self.alt = np.zeros([N])                    # Altitude [ft/m] TODO: define altitude unit

        # Orientation
        self.heading = np.zeros(N)                  # Heading [deg]
        self.track_angle = np.zeros([N])            # Track angle [deg]
        self.bank_angle = np.zeros([N])             # Bank angle [deg]

        # Speed
        self.ias = np.zeros([N])                    # Indicated air speed [knot]
        self.cas = np.zeros([N])                    # Calibrated air speed [knot]
        self.tas = np.zeros([N])                    # True air speed [knot]
        self.gs = np.zeros(N)                       # Ground speed [knot]
        self.mach = np.zeros([N])                   # Mach number [dimensionless]
        self.vs = np.zeros([N])                     # Vertical speed [ft/min]

        # Weight and balance
        self.weight = np.zeros([N])                 # Aircraft weight [kg]
        self.fuel_weight = np.zeros([N])            # Fuel weight [kg]
        self.payload_weight = np.zeros([N])         # Payload weight [kg]



        pass