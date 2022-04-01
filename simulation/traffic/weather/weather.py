import numpy as np
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from traffic.performance.performance import Performance
from utils.unit import Unit_conversion
from traffic.weather.era5 import Era5


class Weather:
    
    def __init__(self, N, start_time, end_time):
        self.mode = "ISA"
        """Weather mode [ISA, ERA5]"""
        self.start_time = start_time

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

        # Download ERA5 data
        self.weather_data = [xr.open_dataset(file) for file in Era5.download_data(start_time, end_time)]
        Era5.generate_wind_barb(self.weather_data[0], time=self.start_time.replace(second=0, minute=0), level=900)


    def add_aircraft(self, n, alt, perf: Performance):
        self.T[n] = perf.cal_temperature(Unit_conversion.feet_to_meter(alt), self.d_T[n])
        self.p[n] = perf.cal_air_pressure(Unit_conversion.feet_to_meter(alt), self.T[n], self.d_T[n])
        self.rho[n] = perf.cal_air_density(self.p[n], self.T[n])


    def update(self, lat, long, alt, perf: Performance, global_time):
        self.T = perf.cal_temperature(Unit_conversion.feet_to_meter(alt), self.d_T)
        self.p = perf.cal_air_pressure(Unit_conversion.feet_to_meter(alt), self.T, self.d_T)
        self.rho = perf.cal_air_density(self.p, self.T)
        ds = self.weather_data[0].sel(longitude=xr.DataArray(long, dims="points"), latitude=xr.DataArray(lat, dims="points"), time=np.datetime64((self.start_time+timedelta(seconds=global_time)).replace(second=0, minute=0),'ns'), method="ffill") # 
        index = np.array([np.searchsorted(-x, -Unit_conversion.feet_to_meter(alt)*9.80665, side='right') for x, alt in zip(ds['z'].values.T, alt)])
        self.wind_east = Unit_conversion.mps_to_knots(np.array([x[i] for x, i in zip(ds['u'].values.T, index)]))
        self.wind_north = Unit_conversion.mps_to_knots(np.array([x[i] for x, i in zip(ds['v'].values.T, index)]))