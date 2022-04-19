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
        if Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/'+file_name+'.nc').exists():
            print ("ERA5 data exists.")
        else :
            print("Downloading ERA5 data.")
            print("Downlad expected to complete in 10 minutes. Visit https://cds.climate.copernicus.eu/cdsapp#!/yourrequests for the status of the request. \n")
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
                'data/weather/'+file_name+'.nc')
        return Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/'+file_name+'.nc')


    @staticmethod
    def generate_wind_barb(datasource, time, level):
        
        data = datasource.sel(level=level, time=time)
        # p = data.t.plot(subplot_kws=dict(projection=ccrs.Orthographic(30, 20)),transform=ccrs.PlateCarree(),)
        # p.axes.set_global()
        # p.axes.coastlines()
        # plt.savefig('cartopy_example.png')
        fig = Figure(figsize=(100, 50), ) #facecolor='none'
        ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(), frameon=False)
        # ax.set_extent([-90, 80, 10, 85], crs=ccrs.PlateCarree())
        ax.set_global()
        ax.coastlines()  
        skip = 10
        ax.barbs(data.longitude.values[::skip], data.latitude.values[::skip], data.u.values[::skip, ::skip], data.v.values[::skip, ::skip], 
                # length=5, sizes=dict(emptybarb=0.25, spacing=0.2, height=0.5), linewidth=0.95, 
                transform=ccrs.PlateCarree())
        buf = BytesIO()
        fig.savefig(buf, format="png", transparent=True)
        uri = 'data:image/png;base64,' + base64.b64encode(buf.getbuffer()).decode("ascii")
        print(uri)
        fig.savefig('barb.png', transparent=True)
        return uri


    @staticmethod
    def generate_specific_rain_water_content(datasource, time, level):
        
        data = datasource.sel(level=level, time=time)
        # p = data.t.plot(subplot_kws=dict(projection=ccrs.Orthographic(30, 20)),transform=ccrs.PlateCarree(),)
        # p.axes.set_global()
        # p.axes.coastlines()
        # plt.savefig('cartopy_example.png')
        fig = Figure(figsize=(100, 50), ) #facecolor='none'
        ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(), frameon=False)
        # ax.set_extent([-90, 80, 10, 85], crs=ccrs.PlateCarree())
        ax.set_global()
        ax.coastlines()  
        skip = 10
        ax.barbs(data.longitude.values[::skip], data.latitude.values[::skip], data.u.values[::skip, ::skip], data.v.values[::skip, ::skip], 
                # length=5, sizes=dict(emptybarb=0.25, spacing=0.2, height=0.5), linewidth=0.95, 
                transform=ccrs.PlateCarree())
        buf = BytesIO()
        fig.savefig(buf, format="png", transparent=True)
        uri = 'data:image/png;base64,' + base64.b64encode(buf.getbuffer()).decode("ascii")
        print(uri)
        fig.savefig('barb.png', transparent=True)
        return uri
