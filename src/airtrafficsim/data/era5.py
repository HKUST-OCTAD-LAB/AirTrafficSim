"""
Google Research's [Analysis-Ready & Cloud Optimized (ARCO) ERA5](https://github.com/google-research/arco-era5)
dataset

Format: `netcdf`, indexed by the specific date and pressure level.

See:

- https://cloud.google.com/storage/docs/public-datasets/era5
- https://github.com/google-research/arco-era5

Data License: [Copernicus license](https://apps.ecmwf.int/datasets/licences/copernicus/)

Requires:

- `gcloud` CLI to be installed and authenticated
- airtrafficsim installed with extras `network`, `polars`, `era5`
"""

# TODO: use cdsapi as a fallback

import random
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Generator, NamedTuple

import polars as pl
import pytz
import xarray as xr

from .. import logger
from ..annotations import StaticTemperature, WindSpeed
from ..performance.bada3 import atmosphere

if TYPE_CHECKING:
    from typing import Annotated

    from ..annotations import StaticPressure

GOOGLE_STORAGE_URI = (
    "gs://gcp-public-data-arco-era5/raw/date-variable-pressure_level"
)
PRESSURE_LEVELS: Annotated[tuple[int], StaticPressure("hPa")] = (
    *range(100, 275, 25),
    *range(300, 750, 50),
    *range(750, 1025, 25),
)


class EcmwfParameter(NamedTuple):
    id_: int
    name: str
    short_name: str
    quantity: str | object


VARIABLES: list[EcmwfParameter] = [
    EcmwfParameter(248, "fraction_of_cloud_cover", "cc", "0-1"),
    EcmwfParameter(129, "geopotential", "z", "m² s⁻²"),
    EcmwfParameter(203, "ozone_mass_mixing_ratio", "o3", "kg kg⁻¹"),
    EcmwfParameter(60, "potential_vorticity", "pv", "s⁻¹"),
    EcmwfParameter(247, "specific_cloud_ice_water_content", "ciwc", "kg kg⁻¹"),
    EcmwfParameter(
        246, "specific_cloud_liquid_water_content", "clwc", "kg kg⁻¹"
    ),
    EcmwfParameter(133, "specific_humidity", "q", "kg kg⁻¹"),
    EcmwfParameter(130, "temperature", "t", StaticTemperature("K")),
    EcmwfParameter(131, "u_component_of_wind", "u", WindSpeed("m s⁻¹")),
    EcmwfParameter(132, "v_component_of_wind", "v", WindSpeed("m s⁻¹")),
    EcmwfParameter(135, "vertical_velocity", "w", "Pa s⁻¹"),
]
"""Available variables under the `raw` bucket."""
VARIABLES_MAP = {v.name: v.short_name for v in VARIABLES}


def dates(start: datetime, end: datetime) -> Generator[str, None, None]:
    """
    Generate dates in the format `YYYY/MM/DD` from start to end, inclusive.
    """
    curr = start
    while curr <= end:
        yield curr.strftime("%Y/%m/%d")
        curr += timedelta(days=1)


# TODO: instead of subprocess, use the official library
def fetch_weather(
    date_start: datetime = datetime(2023, 2, 1, tzinfo=pytz.utc),
    date_end: datetime = datetime(2023, 2, 1, tzinfo=pytz.utc),
    *,
    base_dir: Path,
    variables: list[str] = list(VARIABLES_MAP.keys()),
    pressure_levels: tuple[int] = PRESSURE_LEVELS,
    gs_base: str = GOOGLE_STORAGE_URI,
) -> None:
    """
    Recursively download all global ERA5 data for the specified date
    interval, pressure levels and variables as NetCDF files.

    The directory structure will be mirrored as:
    `{base_dir}/{YYYY}/{MM}/{DD}/{variable_name}/{pressure_level}.nc`.
    """
    for date in dates(date_start, date_end):
        for variable in variables:
            path_out = base_dir / date / variable
            path_out.mkdir(parents=True, exist_ok=True)

            queue = []
            for level in pressure_levels:
                fp_relative = Path(date) / variable / f"{level}.nc"
                if (base_dir / fp_relative).is_file():
                    continue
                queue.append(f"{gs_base}/{fp_relative}".encode())
            if not queue:
                logger.info(f"{path_out}: skipping, all exists")
                continue
            logger.info(f"{path_out}: downloading {len(queue)}")
            subprocess.check_output(
                ["gcloud", "storage", "cp", "-I", str(path_out)],
                input=b"\n".join(queue),
            )


def concat_dataset(
    variable: str,
    base_dir_date: Path,
) -> xr.Dataset:
    """
    Concatenates all pressure levels for a given variable and date
    into a single dataset

    Example:

    ```txt
    <xarray.Dataset> Size: 5GB
    Dimensions:    (isobaricInhPa: 27, time: 24, latitude: 721, longitude: 1440)
    Coordinates:
    * longitude    (longitude) float32 6kB 0.0 0.25 0.5 ... 359.2 359.5 359.8
    * latitude     (latitude) float32 3kB 90.0 89.75 89.5 ... -89.5 -89.75 -90.0
    * time         (time) datetime64[ns] 192B 2023-02-01 ... 2023-02-01T23:00:00
    * isobaricInhPa  (isobaricInhPa) int64 216B 100 1000 125 150 ... 925 950 975
    Data variables:
        z      (isobaricInhPa, time, latitude, longitude) float64 5GB dask.array
        <chunksize=(1, 24, 721, 1440), meta=np.ndarray>
    Attributes:
        Conventions:  CF-1.6
        history:  2023-06-24 08:54:57 GMT by grib_to_netcdf-2.25.1: /opt/ecmw...
    ```
    """

    weather_variable = base_dir_date / variable
    weather_variable_fps = list(
        sorted(
            weather_variable.glob("*.nc"),
            key=lambda x: int(x.stem),
            reverse=True,
        )
    )
    logger.debug(
        f"reading {variable=}, found {len(weather_variable_fps)} nc files"
    )

    # NOTE: the pressure dimension is not included in each file - we generate
    # placeholders to be later overwritten
    def add_dummy_pressure_dim(ds: xr.Dataset) -> xr.Dataset:
        ds = ds.expand_dims(isobaricInhPa=[random.uniform(100, 1000)])
        return ds

    ds = xr.open_mfdataset(
        weather_variable_fps,
        engine="netcdf4",
        concat_dim="isobaricInhPa",
        combine="nested",
        preprocess=add_dummy_pressure_dim,
    ).assign_coords(isobaricInhPa=[int(fp.stem) for fp in weather_variable_fps])

    return ds


def build_path(base_dir: Path, year: int, month: int, day: int) -> Path:
    return base_dir / f"{year:04d}" / f"{month:02d}" / f"{day:02d}"


# TODO: do not hardcode base_dir_date - we cannot assume trajectory
# spans a single day
# TODO: break down into smaller functions
def get_data_for_trajectory(
    trajectory: pl.LazyFrame,
    *,
    base_dir: Path,
    year: int,
    month: int,
    day: int,
) -> pl.LazyFrame:
    """
    Extract weather data for the given trajectory

    :return: a lazyframe with the weather data
    """
    base_dir_date = build_path(base_dir, year, month, day)
    time, longitude, latitude, alt = trajectory.select(
        pl.from_epoch(pl.col("timestamp"), time_unit="s"),  # datetime64
        (pl.col("longitude").degrees() + 180),  # [0, 360]
        pl.col("latitude").degrees(),  # [-90, 90]
        pl.col("altitude"),  # meters
    ).collect()

    atmos = atmosphere(alt.to_numpy(), delta_temperature=0)

    times_ = xr.DataArray(time.to_numpy(), dims=["points"])
    lons_ = xr.DataArray(longitude, dims=["points"])
    lats_ = xr.DataArray(latitude, dims=["points"])
    pressures_ = xr.DataArray(atmos.pressure / 100, dims=["points"])  # hPa

    weather = {}
    for variable_name, variable_key in VARIABLES_MAP.items():
        ds = concat_dataset(variable_name, base_dir_date)
        values = ds.interp(
            time=times_,
            latitude=lats_,
            longitude=lons_,
            isobaricInhPa=pressures_,
            kwargs={"fill_value": None},
        )
        values_np = values[variable_key].values
        weather[variable_name] = values_np

    lf = pl.LazyFrame(weather)
    return lf
