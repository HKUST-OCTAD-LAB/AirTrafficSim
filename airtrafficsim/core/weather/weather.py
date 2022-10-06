import numpy as np
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from airtrafficsim.core.performance.performance import Performance
from airtrafficsim.utils.unit_conversion import Unit
from airtrafficsim.core.weather.era5 import Era5


class Weather:
    
    def __init__(self, start_time, end_time, weather_mode, file_name):
        self.mode = weather_mode
        """Weather mode [ISA, ERA5]"""
        self.start_time = start_time

        # Wind speed
        self.wind_speed = np.zeros([0])                         # Wind speed [knots]
        self.wind_direction = np.zeros([0])                     # Wind direction [deg]
        self.wind_north = np.zeros([0])                         # Wind - North [knots]
        self.wind_east = np.zeros([0])                          # Wind - East [knots]
        
        # Atmospheric condition
        self.d_T = np.zeros([0])                                # Temperature difference compare to ISA [K]
        self.d_p = np.zeros([0])                                # Pressure difference compare to ISA [Pa]
        self.T = np.zeros([0])                                  # Temperature [K]
        self.p = np.zeros([0])                                  # Pressure [Pa]
        self.rho = np.zeros([0])                                # Density [kg/m^3]
    
        # Download ERA5 data
        if self.mode == "ERA5":
            multilevel, surface = Era5.download_data(start_time, end_time, file_name)
            self.weather_data = xr.open_dataset(multilevel)
            self.radar_data = xr.open_dataset(surface)



    def add_aircraft(self, alt, perf: Performance):
        self.wind_speed = np.append(self.wind_speed, 0.0)
        self.wind_direction = np.append(self.wind_direction, 0.0)
        self.wind_north = np.append(self.wind_north, 0.0)
        self.wind_east = np.append(self.wind_east, 0.0)
        self.d_T = np.append(self.d_T, 0.0)
        self.d_p = np.append(self.d_p, 0.0)
        self.T = np.append(self.T, perf.cal_temperature(Unit.ft2m(alt), self.d_T[-1]))
        self.p = np.append(self.p, perf.cal_air_pressure(Unit.ft2m(alt), self.T[-1], self.d_T[-1]))
        self.rho = np.append(self.rho, perf.cal_air_density(self.p[-1], self.T[-1]))


    def del_aircraft(self, index):
        self.wind_speed = np.delete(self.wind_speed, index)
        self.wind_direction = np.delete(self.wind_direction, index)
        self.wind_north = np.delete(self.wind_north, index)
        self.wind_east = np.delete(self.wind_east, index)
        self.d_T = np.delete(self.d_T, index)
        self.d_p = np.delete(self.d_p, index)
        self.T = np.delete(self.T, index)
        self.p = np.delete(self.p, index)
        self.rho = np.delete(self.rho, index)


    def update(self, lat, long, alt, perf: Performance, global_time):
        if self.mode == "ERA5":
            ds = self.weather_data.sel(longitude=xr.DataArray(long, dims="points"), latitude=xr.DataArray(lat, dims="points"), time=np.datetime64((self.start_time+timedelta(seconds=global_time)).replace(second=0, minute=0),'ns'), method="ffill") # 
            index = np.array([np.searchsorted(-x, -Unit.ft2m(alt) * 9.80665, side='right') for x, alt in zip(ds['z'].values.T, alt)]) - 1
            temp = np.array([x[i] for x, i in zip(ds['t'].values.T, index)])
            self.d_T = temp - perf.cal_temperature(Unit.ft2m(alt), 0.0)
            self.wind_east = Unit.mps2kts(np.array([x[i] for x, i in zip(ds['u'].values.T, index)]))
            self.wind_north = Unit.mps2kts(np.array([x[i] for x, i in zip(ds['v'].values.T, index)]))

        self.T = perf.cal_temperature(Unit.ft2m(alt), self.d_T)
        self.p = perf.cal_air_pressure(Unit.ft2m(alt), self.T, self.d_T)
        self.rho = perf.cal_air_density(self.p, self.T)