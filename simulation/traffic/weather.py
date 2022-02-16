import numpy as np

class Weather:
    
    def __init__(self, N=1000):
        # Turbulence
        self.wind_north = np.zeros([N])                         # Wind - North [knots]
        self.wind_east = np.zeros([N])                          # Wind - East [knots]
        
        # Atmospheric condition
        self.d_T = np.zeros([N])                                # Temperature difference compare to ISA [K]
        self.d_p = np.zeros([N])                                # Pressure difference compare to ISA [Pa]
        self.T = np.zeros([N])                                  # Temperature [K]
        self.p = np.zeros([N])                                  # Pressure [Pa]
        self.rho = np.zeros([N])                                # Density [kg/m^3]