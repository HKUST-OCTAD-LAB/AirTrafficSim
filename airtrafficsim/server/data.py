from pathlib import Path
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib import colors
import numpy as np
import xarray as xr
import cartopy.crs as ccrs
from PIL import Image
from io import BytesIO
import base64
from airtrafficsim.core.navigation import Nav

class Data:
    @staticmethod
    def get_nav(lat1, long1, lat2, long2):
        """
        Get the navigation waypoint data given
        
        Parameters
        ----------
        lat1 : float
            Latitude (South)
        long1 : float
            Longitude (West)
        lat2 : float
            Latitude (North)
        long2 : float
            Longitude (East)

        Returns
        -------
        {}
            JSON CZML file of navigation waypoint data
        """

        document = [{
            "id": "document",
            "name": "Nav",
            "version": "1.0",
        }]

        fixes = Nav.get_wp_in_area(lat1, long1, lat2, long2)

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
    def get_era5_wind(file, lat1, long1, lat2, long2, time):
        """
        Get the ERA5 wind data image to client
        
        Parameters
        ----------
        lat1 : float
            Latitude (South)
        long1 : float
            Longitude (West)
        lat2 : float
            Latitude (North)
        long2 : float
            Longitude (East)

        Returns
        -------
        {}
            JSON CZML file of ERA5 wind data image
        """
        # TODO: Improve data loading to avoid repetitive loading
        if Path(__file__).parent.parent.parent.joinpath('data/weather/era5/',file.split('-', 1)[0]).is_dir():
            data = xr.open_dataset(Path(__file__).parent.parent.parent.joinpath('data/weather/era5/',file.split('-', 1)[0]+'/multilevel.nc')).sel(level=900, time=datetime.fromisoformat(time), method="pad")
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
    def get_era5_rain(file, lat1, long1, lat2, long2, time):
        """
        Get the ERA5 rain data image to client
        
        Parameters
        ----------
        lat1 : float
            Latitude (South)
        long1 : float
            Longitude (West)
        lat2 : float
            Latitude (North)
        long2 : float
            Longitude (East)

        Returns
        -------
        {}
            JSON CZML file of ERA5 rain data image
        """
        # TODO: Improve data loading to avoid repetitive loading
        if Path(__file__).parent.parent.parent.joinpath('data/weather/era5/',file.split('-', 1)[0]).is_dir():
            data = xr.open_dataset(Path(__file__).parent.parent.parent.joinpath('data/weather/era5/',file.split('-', 1)[0]+'/surface.nc')).sel(time=datetime.fromisoformat(time), method="pad")
            data = data.where((((data.latitude >= lat1) & (data.latitude <= lat2)) & ((data.longitude >= (long1+360.0) % 360.0) & (data.longitude <= (long2+360.0) % 360.0))), drop=True)
            fig = Figure(figsize=(long2-long1, lat2-lat1), facecolor='none', dpi=500)
            # fig = Figure(figsize=(360, 180), facecolor='none', dpi=100)
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


    @staticmethod
    def get_radar_img(file, lat1, long1, lat2, long2, time):
        """
        Get the radar data image to client
        
        Parameters
        ----------
        lat1 : float
            Latitude (South)
        long1 : float
            Longitude (West)
        lat2 : float
            Latitude (North)
        long2 : float
            Longitude (East)
        time : string
            Time in ISO format
        file : string
            File name of the radar image

        Returns
        -------
        {}
            JSON CZML file of radar data image
        """
        # TODO: Expand to other data source
        lat1 = 22.3022 - 2.3152
        long1 = 114.1742 - 2.3152
        lat2 = 22.3022 + 2.3152
        long2 = 114.1742 + 2.3152
        # Definition
        rain_fall   = np.array([0.15, 0.5,   1,   2,   3,   5,   7,  10,  15,  30,  50,  75, 100, 150, 200, 300,   0,   0,   0])    # Minimum value of rainfall rate category
        rain_fall_r = np.array([   0,   0,  60,   0,   0,   0,   0, 145, 225, 255, 240, 240, 240, 200, 200, 240, 211, 116, 148], dtype=float)
        rain_fall_g = np.array([ 200, 145, 150, 130, 170, 210, 250, 255, 210, 210, 175, 130,   0,   0,   0,   0, 155, 117, 109], dtype=float)
        rain_fall_b = np.array([ 250, 245, 255,  70,  55,   0,   5,   0,   0,   0,   0,   0,   0,   0, 105, 240,  94, 199,  66], dtype=float)

        colorsList = ['#ffffff00', '#00c9fc', '#008ff4', '#3b96ff', '#018445', '#01aa35', '#00cf01', '#00f906', '#91ff00',
          '#e0d000', '#ffd201', '#efb001', '#f08002', '#f00001', '#ce0101', '#bc016a', '#ef00f0']
        scale = [0, 0.15, 0.5, 1, 2, 3, 5, 7, 10, 15, 30, 50, 75, 100, 150, 200, 300]

        # Input
        if Path(__file__).parent.parent.parent.joinpath('data/weather/radar/',file.split('-', 1)[0]).is_dir():
            for file in Path(__file__).parent.parent.parent.joinpath('data/weather/radar/',file.split('-', 1)[0]).iterdir():
                if (datetime.fromisoformat(time+'+00:00') - datetime.fromisoformat(file.stem+'+00:00')).seconds < 3600:
                    img = Image.open(file, 'r')
                    #Cut the color bar and description
                    left = 0
                    top = 0
                    right = 400
                    bottom = 400
                    img = img.crop((left, top, right, bottom)) 
                    data = np.array(img)

                    # Computer square distance of color https://en.wikipedia.org/wiki/Color_difference
                    distant = [np.square(data[:,:,0].flatten() - rain_fall_r[i]) + np.square(data[:,:,1].flatten() - rain_fall_g[i]) + np.square(data[:,:,2].flatten() - rain_fall_b[i]) for i in range(len(rain_fall))]
                    distant = np.stack(distant, axis=-1)
                    # Find the index of minimum element row-wise in distance array
                    index = np.argmin(distant, axis = 1)
                    # Grab the rain_fall category value given index of rain_fall array
                    result = np.take(rain_fall, index)
                    # Check if the minimum distance is smaller than a confidence interval
                    CONFIDENCE = 6000.0
                    min_distant = np.amin(distant, axis=1)
                    result = np.where(min_distant < CONFIDENCE, result, 0)
                    result = result.reshape(np.abs(bottom-top), np.abs(right-left))

                    # Plot 
                    fig = Figure(figsize=(long2-long1, lat2-lat1), facecolor='none', dpi=500)
                    ax = fig.add_axes([0, 0, 1, 1], frameon=False)
                    # ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree(), frameon=False)
                    # ax.set_extent([long1, long2, lat1, lat2], crs=ccrs.PlateCarree())
                    cmap=colors.ListedColormap(colorsList)
                    norm=colors.BoundaryNorm(scale, len(colorsList))
                    ax.imshow(result, cmap=cmap, norm=norm)
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
