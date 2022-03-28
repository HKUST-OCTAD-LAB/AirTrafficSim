import numpy as np
from traffic.performance import Performance
from utils.unit import Unit_conversion

import cdsapi
c = cdsapi.Client()
# c.retrieve(
#     'reanalysis-era5-pressure-levels',
#     {
#         'product_type': 'reanalysis',
#         'format': 'grib',
#         'variable': 'temperature',
#         'pressure_level': '1',
#         'year': '2018',
#         'month': '09',
#         'day': '15',
#         'time': '08:00',
#     },
#     'data/weather/download.grib')

class Weather:
    
    def __init__(self, N=1000):
        # Wind speed
        self.wind_speed = np.zeros([N])                         # Wind speed [knots]
        self.wind_direction = np.zeros([N])                     # Wind direction [deg]
        self.wind_north = np.zeros([N])                         # Wind - North [knots]
        self.wind_east = np.zeros([N])                          # Wind - East [knots]
        
        # Atmospheric condition
        self.d_T = np.zeros([N])                                # Temperature difference compare to ISA [K]
        self.d_p = np.zeros([N])                                # Pressure difference compare to ISA [Pa]
        self.T = np.zeros([N])                                  # Temperature [K]
        self.p = np.zeros([N])                                  # Pressure [Pa]
        self.rho = np.zeros([N])                                # Density [kg/m^3]

    def add_aircraft(self, n, alt, perf: Performance):
        self.T[n] = perf.cal_temperature(Unit_conversion.feet_to_meter(alt), self.d_T[n])
        self.p[n] = perf.cal_air_pressure(Unit_conversion.feet_to_meter(alt), self.T[n], self.d_T[n])
        self.rho[n] = perf.cal_air_density(self.p[n], self.T[n])


    def update(self, alt, perf: Performance):
        self.T = perf.cal_temperature(Unit_conversion.feet_to_meter(alt), self.d_T)
        self.p = perf.cal_air_pressure(Unit_conversion.feet_to_meter(alt), self.T, self.d_T)
        self.rho = perf.cal_air_density(self.p, self.T)