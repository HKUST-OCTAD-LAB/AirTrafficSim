from traffic.nav import Nav
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib import colors
import xarray as xr
import cartopy.crs as ccrs
from io import BytesIO
import base64

class Utils:
    @staticmethod
    def get_nav(lat1, long1, lat2, long2):
        document = [{
            "id": "document",
            "name": "Nav",
            "version": "1.0",
        }]

        fixes = Nav.get_fix_in_area(lat1, long1, lat2, long2)

        for fix in fixes:
            document.append({
                "id": fix[2],
                "position": {
                    "cartographicDegrees": [fix[1], fix[0], 0]
                },
                "point": {
                    "pixelSize": 4,
                    "color": {
                        "rgba": [39, 243, 245, 240]
                    }
                },
                "label": {
                    "text": fix[2],
                    "font": "9px sans-serif",
                    "horizontalOrigin": "LEFT",
                    "pixelOffset": {
                        "cartesian2": [10, 0],
                    },
                    # "distanceDisplayCondition": {
                    #     "distanceDisplayCondition": [0, 1000000]
                    # },
                    # "showBackground": "true",
                    # "backgroundColor": {
                    #     "rgba": [0, 0, 0, 50]
                    # }
                }
            })

        return document


    @staticmethod
    def get_wind_bard(lat1, long1, lat2, long2):
        data = xr.open_dataset('data/weather/FullFlightDemo/multilevel.nc').sel(level=900, time=datetime.fromisoformat('2022-03-22T00:00:00'))
        data = data.where((((data.latitude >= lat1) & (data.latitude <= lat2)) & ((data.longitude >= (long1+360.0) % 360.0) & (data.longitude <= (long2+360.0) % 360.0))), drop=True)
        fig = Figure(figsize=(long2-long1, lat2-lat1), facecolor='none', dpi=500)
        ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(), frameon=False)
        ax.set_extent([long1, long2, lat1, lat2], crs=ccrs.PlateCarree())
        # ax.set_global()
        # ax.coastlines()  
        ax.barbs(data.longitude.values, data.latitude.values, data.u.values, data.v.values, 
                flagcolor='grey',
                # sizes=dict(emptybarb=0.25, spacing=0.2, height=0.5), linewidth=0.95, length=5, 
                transform=ccrs.PlateCarree())
        buf = BytesIO()
        fig.savefig(buf, format="png")
        uri = "data:image/png;base64," + base64.b64encode(buf.getbuffer()).decode("ascii")
        return [
            {
                "id": "document",
                "name": "Weather",
                "version": "1.0",
            },
            {
                "id": "Weather",
                "rectangle": {
                    "coordinates": {
                        "wsenDegrees": [long1, lat1, long2, lat2],
                    },
                    "height": 0,
                    "fill": True,
                    "material": {
                        "image": {
                            "image": { "uri": uri },
                            "color": {
                                "rgba": [255, 255, 255, 128],
                            },
                            "transparent": True,
                        },
                    },
                },
            },
        ]

    @staticmethod
    def get_radar_img(lat1, long1, lat2, long2):
        data = xr.open_dataset('data/weather/FullFlightDemo/surface.nc').sel(time=datetime.fromisoformat('2022-03-22T00:00:00'))
        data = data.where((((data.latitude >= lat1) & (data.latitude <= lat2)) & ((data.longitude >= (long1+360.0) % 360.0) & (data.longitude <= (long2+360.0) % 360.0))), drop=True)
        fig = Figure(figsize=(long2-long1, lat2-lat1), facecolor='none', dpi=500)
        ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(), frameon=False)
        ax.set_extent([long1, long2, lat1, lat2], crs=ccrs.PlateCarree())
        # ax.set_global()
        # ax.coastlines() 
        colorscale = ['#ffffff00', '#00c9fc', '#008ff4', '#3b96ff', '#018445', '#01aa35', '#00cf01', '#00f906', '#91ff00',
                      '#e0d000', '#ffd201', '#efb001', '#f08002', '#f00001', '#ce0101', '#bc016a', '#ef00f0']
        scale = [0, 0.15, 0.5, 1, 2, 3, 5, 7, 10, 15, 30, 50, 75, 100, 150, 200, 300]
        cmap=colors.ListedColormap(colorscale)
        norm=colors.BoundaryNorm(scale, len(colorscale))
        ax.pcolormesh(data.longitude.values, data.latitude.values, data.tp.values*75625.0,
                cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
        buf = BytesIO()
        fig.savefig(buf, format="png")
        uri = "data:image/png;base64," + base64.b64encode(buf.getbuffer()).decode("ascii")
        return [
            {
                "id": "document",
                "name": "Weather",
                "version": "1.0",
            },
            {
                "id": "Weather",
                "rectangle": {
                    "coordinates": {
                        "wsenDegrees": [long1, lat1, long2, lat2],
                    },
                    "height": 0,
                    "fill": True,
                    "material": {
                        "image": {
                            "image": { "uri": uri },
                            "color": {
                                "rgba": [255, 255, 255, 120],
                            },
                            "transparent": True,
                        },
                    },
                },
            },
        ]