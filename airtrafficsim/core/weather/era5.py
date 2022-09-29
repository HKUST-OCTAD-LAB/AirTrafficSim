from traceback import print_tb
import cdsapi
from datetime import datetime, timedelta, time
from pathlib import Path
from matplotlib.figure import Figure
import xarray as xr
import cartopy.crs as ccrs
from io import BytesIO
import base64

class Era5:
    """
    A utility class to handle ERA5 weather data
    """

    @staticmethod
    def download_data(start_time: datetime, end_time: datetime, file_name):
        c = cdsapi.Client()
        if Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/era5/'+file_name).exists() and any(Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/era5/'+file_name).iterdir()):
            print ("ERA5 data exists.")
        else :
            print("Downloading ERA5 data.")
            print("Downlad expected to complete in few minutes. Visit https://cds.climate.copernicus.eu/cdsapp#!/yourrequests for the status of the request. \n")
            if not Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/era5/'+file_name).exists():
                Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/era5/'+file_name).mkdir()
            tmp = start_time
            year = []
            month = []
            day = []
            hour = []
            while(tmp < start_time + timedelta(seconds=end_time)):
                if not year or str(tmp.year) != year[-1]:
                    year.append(str(tmp.year))
                if not month or str(tmp.month) != month[-1]:
                    month.append(str(tmp.month))
                if not day or str(tmp.day) != day[-1]:
                    day.append(str(tmp.day))
                if not hour or time(hour=tmp.hour).isoformat(timespec='minutes') != hour[-1]:
                    hour.append(time(hour=tmp.hour).isoformat(timespec='minutes'))
                tmp += timedelta(hours=1)

            c.retrieve(
                'reanalysis-era5-pressure-levels',
                {
                    'product_type': 'reanalysis',
                    'variable': [
                        'geopotential', 'temperature', 'u_component_of_wind',
                        'v_component_of_wind',
                    ],
                    'pressure_level': [
                        '50',  '70', '100', 
                        '125', '150', '175', 
                        '200', '225', '250', 
                        '300', '350', '400', 
                        '450', '500', '550', 
                        '600', '650', '700', 
                        '750', '775', '800', 
                        '825', '850', '875', 
                        '900', '925', '950', 
                        '975', '1000',
                    ],
                    'year': year,
                    'month': month,
                    'day': day,
                    'time': hour,
                    # 'area': [ 90, 0, 0, 90,],       #North, West, South, East
                    'format': 'netcdf',
                },
                Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/era5/'+file_name+'/multilevel.nc'))
        
            c.retrieve(
                'reanalysis-era5-single-levels',
                {
                    'product_type': 'reanalysis',
                    'format': 'netcdf',
                    'variable': 'total_precipitation',
                    'year': year,
                    'month': month,
                    'day': day,
                    'time': hour,
                },
                Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/era5/'+file_name+'/surface.nc'))
        
        return Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/era5/'+file_name+'/multilevel.nc'), Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/era5/'+file_name+'/surface.nc')
