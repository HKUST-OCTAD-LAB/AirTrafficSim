from datetime import datetime, timedelta
from typing import Literal, TypeAlias

import xarray as xr

import numpy as np

from ...types import array
from ...utils.unit_conversion import Unit
from ..performance.performance import Performance
from ..weather.era5 import Era5

WeatherMode: TypeAlias = Literal["ISA", "ERA5", ""]
# TODO(abrah): repalce with str | None instead of this.


class Weather:
    def __init__(
        self,
        start_time: datetime,
        duration_s: float,
        weather_mode: WeatherMode,
        file_name: str,
    ) -> None:
        """
        Weather class constructor

        Parameters
        ----------
        start_time : datetime
            Start time of the simulation
        duration_s : float
            Duration of the simulation
        weather_mode : str
            Weather mode [ISA, ERA5]
        file_name : str
            File name of the weather data
        """
        self.weather_mode = weather_mode
        """Weather mode [ISA, ERA5]"""
        self.start_time = start_time
        """Start time of the simulation [datetime]"""

        # Wind speed
        self.wind_speed = np.zeros([0])
        """Wind speed [knots]"""
        self.wind_direction = np.zeros([0])
        """Wind direction [deg]"""
        self.wind_north = np.zeros([0])
        """Wind - North [knots]"""
        self.wind_east = np.zeros([0])
        """Wind - East [knots]"""

        # FIXME(abrah): this is duplicated in ..performance. remove this.
        # Atmospheric condition
        self.d_T = np.zeros([0])
        """Temperature difference compare to ISA [K]"""
        self.d_p = np.zeros([0])
        """Pressure difference compare to ISA [Pa]"""
        self.T = np.zeros([0])
        """Temperature [K]"""
        self.p = np.zeros([0])
        """Pressure [Pa]"""
        self.rho = np.zeros([0])
        """Density [kg/m^3]"""

        # Download ERA5 data
        if self.weather_mode == "ERA5":
            multilevel, surface = Era5.download_data(
                start_time, duration_s, file_name
            )
            self.weather_data = xr.open_dataset(multilevel)
            self.radar_data = xr.open_dataset(surface)

    def add_aircraft(self, alt: float, perf: Performance) -> None:
        """
        Add aircraft to the weather class

        Parameters
        ----------
        alt : float
            Altitude of the aircraft [ft]
        perf : Performance
            Performance class
        """
        self.wind_speed = np.append(self.wind_speed, 0.0)
        self.wind_direction = np.append(self.wind_direction, 0.0)
        self.wind_north = np.append(self.wind_north, 0.0)
        self.wind_east = np.append(self.wind_east, 0.0)
        self.d_T = np.append(self.d_T, 0.0)
        self.d_p = np.append(self.d_p, 0.0)
        self.T = np.append(
            self.T, perf.cal_temperature(Unit.ft2m(alt), self.d_T[-1])
        )
        self.p = np.append(
            self.p,
            perf.cal_air_pressure(Unit.ft2m(alt), self.T[-1], self.d_T[-1]),
        )
        self.rho = np.append(
            self.rho, perf.cal_air_density(self.p[-1], self.T[-1])
        )

    def del_aircraft(self, index: int) -> None:
        """
        Delete aircraft from the weather class

        Parameters
        ----------
        index : int
            Index of the aircraft
        """
        self.wind_speed = np.delete(self.wind_speed, index)
        self.wind_direction = np.delete(self.wind_direction, index)
        self.wind_north = np.delete(self.wind_north, index)
        self.wind_east = np.delete(self.wind_east, index)
        self.d_T = np.delete(self.d_T, index)
        self.d_p = np.delete(self.d_p, index)
        self.T = np.delete(self.T, index)
        self.p = np.delete(self.p, index)
        self.rho = np.delete(self.rho, index)

    def update(
        self,
        lat: array,
        long: array,
        alt: array,
        perf: Performance,
        seconds_since_start: float,
    ) -> None:
        """
        Update weather data

        Parameters
        ----------
        lat : float[]
            Latitude of the aircraft [deg]
        long : float[]
            Longitude of the aircraft [deg]
        alt : float[]
            Altitude of the aircraft [ft]
        perf : Performance
            Performance class
        seconds_since_start : float
            Time since the start of the simulation [seconds]
        """
        if self.weather_mode == "ERA5":
            ds = self.weather_data.sel(
                longitude=xr.DataArray(long, dims="points"),
                latitude=xr.DataArray(lat, dims="points"),
                time=np.datetime64(
                    (
                        self.start_time + timedelta(seconds=seconds_since_start)
                    ).replace(second=0, minute=0),
                    "ns",
                ),
                method="ffill",
            )
            index = (
                np.array(
                    [
                        np.searchsorted(
                            -x,
                            -Unit.ft2m(alt) * 9.80665,  # type: ignore
                            side="right",
                        )
                        for x, alt in zip(ds["z"].values.T, alt)
                    ]
                )
                - 1
            )
            temp = np.array([x[i] for x, i in zip(ds["t"].values.T, index)])
            self.d_T = temp - perf.cal_temperature(
                Unit.ft2m(alt), np.array(0.0)
            )  # type: ignore
            self.wind_east = Unit.mps2kts(
                np.array([x[i] for x, i in zip(ds["u"].values.T, index)])
            )  # type: ignore
            self.wind_north = Unit.mps2kts(
                np.array([x[i] for x, i in zip(ds["v"].values.T, index)])
            )  # type: ignore

        self.T = perf.cal_temperature(Unit.ft2m(alt), self.d_T)  # type: ignore
        self.p = perf.cal_air_pressure(Unit.ft2m(alt), self.T, self.d_T)  # type: ignore
        self.rho = perf.cal_air_density(self.p, self.T)  # type: ignore
