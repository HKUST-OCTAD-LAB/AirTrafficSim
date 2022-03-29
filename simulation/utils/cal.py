import numpy as np


class Calculation:
    """
    A utility class for calculation
    """

    @staticmethod
    def cal_great_circle_distance(lat1, long1, lat2, long2):
        """
        Calculate great circle distance between two point

        Parameters
        ----------
        lat1 : float[]
            Latitude of first point(s)
        long1 : float[]
            Longitude of first point(s)
        lat2 : float[]
            Latitude of second point(s)
        long2 : float[]
            Longitude of second point(s)

        Returns
        -------
        distance : float[]
            Great circle distance [km]

        Note
        ----
        Haversine distance https://en.wikipedia.org/wiki/Haversine_formula using mean Earth radius 6371.009 for the WGS84 ellipsoid
        """
        return 2.0 * 6371.0 * np.arcsin(np.sqrt(np.square(np.sin((np.deg2rad(lat2) - np.deg2rad(lat1))/2.0)) + np.cos(np.deg2rad(lat1)) * np.cos(np.deg2rad(lat2)) * np.square(np.sin((np.deg2rad(long2) - np.deg2rad(long1))/2.0))))

    
    @staticmethod
    def cal_great_circle_bearing(lat1, long1, lat2, long2):
        """
        Calculate bearing of two points following great circle path 

        Parameters
        ----------
        lat1 : float[]
            Latitude of first point(s)
        long1 : float[]
            Longitude of first point(s)
        lat2 : float[]
            Latitude of second point(s)
        long2 : float[]
            Longitude of second point(s)

        Returns
        -------
        bearing : float[]
            Bearing [deg]

        Note
        ----
        Forward azimuth https://www.movable-type.co.uk/scripts/latlong.html
        """
        return np.mod((np.rad2deg(np.arctan2(np.sin(np.deg2rad(long2-long1)) * np.cos(np.deg2rad(lat2)), np.cos(np.deg2rad(lat1))*np.sin(np.deg2rad(lat2)) - np.sin(np.deg2rad(lat1))*np.cos(np.deg2rad(lat2))*np.cos(np.deg2rad(long2-long1)))) + 360.0), 360.0)

    @staticmethod
    def cal_angle_diff(current_angle, target_angle):
        """
        Calculate the difference of two angle (+ve clockwise, -ve anti-clockwise)

        Parameters
        ----------
        current_angle : float[]
            Current angle
        target_angle : float[]
            Target angle
        """
        return np.mod(target_angle - current_angle + 180.0, 360.0) - 180.0 