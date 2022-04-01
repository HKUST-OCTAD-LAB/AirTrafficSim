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
    def download_data(start_time: datetime, end_time: datetime):
        file_path = []
        c = cdsapi.Client()
        tmp = start_time
        while tmp < (start_time + timedelta(seconds=end_time)):
            if Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/'+tmp.isoformat(timespec="hours")+":00"+'.nc').exists():
                print ("ERA5 data at", tmp.isoformat(timespec="hours")+":00", "exists.")
            else :
                print("Downloading ERA5 data at", tmp.isoformat(timespec="hours")+":00.")
                print("Downlad expected to complete in 10 minutes. Visit https://cds.climate.copernicus.eu/cdsapp#!/yourrequests for the status of the request. \n")
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
                        'year': str(tmp.year),
                        'month': str(tmp.month),
                        'day': str(tmp.day),
                        'time': time(hour=tmp.hour).isoformat(timespec='minutes'),
                        # 'area': [ 90, 0, 0, 90,],       #North, West, South, East
                        'format': 'netcdf',
                    },
                    'data/weather/'+tmp.isoformat(timespec="hours")+":00"+'.nc')
            file_path.append(Path(__file__).parent.parent.parent.parent.resolve().joinpath('data/weather/'+tmp.isoformat(timespec="hours")+":00"+'.nc'))
            tmp += timedelta(hours=1)
        return (file_path)


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
