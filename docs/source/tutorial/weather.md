# Using historical weather database

AirTrafficSim can use [ECMWF ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview) as a weather data source. The `WeatherDemo` class in `environment/WeatherDemo.py` demonstrates how to set up `ERA5` weather mode in AirTrafficSim.

```{code-block} python
---
lineno-start: 11
emphasize-lines: 5
---
# Initialize environment super class
super().__init__(file_name = Path(__file__).name.removesuffix('.py'), #File name (do not change)
                start_time = datetime.fromisoformat('2018-05-01T00:00:00+00:00'),
                end_time = 1000,
                weather_mode = "ERA5",
                performance_mode = "BADA" 
                )
```

To use the historical weather database, set `weather_mode` to "ERA5". This will download the weather data in netCDF format to `data/weather/erea5/<environment name>/`. By default, it is an empty string `""` which will use the International Standard Atmosphere (ISA) for computation and assume 0 winds.

```{attention}

Please ensure that the API key for the weather database from ECMWF Climate Data Store has been set up following [this guide](https://cds.climate.copernicus.eu/api-how-to) to set up .
```

## Usage of al weather data

The downloaded data will be loaded and for each timestep, AirTrafficSim will find the related temperature and wind data at the location and altitude of each aircraft. Then, the temperature temperature information difference with ISA will be used for further atmosphere condition calculation.

```{code-block} python
---
lineno-start: 65
emphasize-lines: 5, 6, 7
caption: weather.py
---
if self.mode == "ERA5":
    ds = self.weather_data.sel(longitude=xr.DataArray(long, dims="points"), latitude=xr.DataArray(lat, dims="points"), time=np.datetime64((self.start_time+timedelta(seconds=global_time)).replace(second=0, minute=0),'ns'), method="ffill") # 
    index = np.array([np.searchsorted(-x, -Unit.ft2m(alt) * 9.80665, side='right') for x, alt in zip(ds['z'].values.T, alt)]) - 1
    temp = np.array([x[i] for x, i in zip(ds['t'].values.T, index)])
    self.d_T = temp - perf.cal_temperature(Unit.ft2m(alt), 0.0)
    self.wind_east = Unit.mps2kts(np.array([x[i] for x, i in zip(ds['u'].values.T, index)]))
    self.wind_north = Unit.mps2kts(np.array([x[i] for x, i in zip(ds['v'].values.T, index)]))
```
