from typing_extensions import deprecated

import numpy as np

from ..types import array

REPLACEMENT = "airtrafficsim.experimental.geospatial"


class Cal:
    """
    A utility class for calculation
    """

    # TODO: refactor to use Point2D namedtuple instead.
    # verify we need it in radians.
    @staticmethod
    @deprecated(REPLACEMENT)
    def cal_great_circle_dist(
        lat1: array, long1: array, lat2: array, long2: array
    ) -> array:
        """
        Calculate great circle distance in km between two point.

        Parameters
        ----------
        lat1 : float[]
            Latitude of first point(s) [deg]
        long1 : float[]
            Longitude of first point(s) [deg]
        lat2 : float[]
            Latitude of second point(s) [deg]
        long2 : float[]
            Longitude of second point(s) [deg]

        Returns
        -------
        float[]
            Great circle distance [km]

        Notes
        -----
        Haversine distance using mean Earth radius 6371.009km for the WGS84
        ellipsoid.
        https://www.movable-type.co.uk/scripts/latlong.html
        """
        a = np.square(np.sin((np.deg2rad(lat2 - lat1)) / 2.0)) + np.cos(
            np.deg2rad(lat1)
        ) * np.cos(np.deg2rad(lat2)) * np.square(
            np.sin((np.deg2rad(long2 - long1)) / 2.0)
        )
        return 2.0 * 6371.009 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))  # type: ignore

    @deprecated(REPLACEMENT)
    @staticmethod
    def cal_great_circle_bearing(
        lat1: array, long1: array, lat2: array, long2: array
    ) -> array:
        """
        Calculate the great circle bearing of two points.

        Parameters
        ----------
        lat1 : float[]
            Latitude of first point(s) [deg]
        long1 : float[]
            Longitude of first point(s) [deg]
        lat2 : float[]
            Latitude of second point(s) [deg]
        long2 : float[]
            Longitude of second point(s) [deg]

        Returns
        -------
        float[]
            Bearing [deg 0-360]

        Notes
        -----
        Initial bearing or forward azimuth
        https://www.movable-type.co.uk/scripts/latlong.html
        """
        bearing = np.mod(
            (
                np.rad2deg(
                    np.arctan2(
                        np.sin(np.deg2rad(long2 - long1))
                        * np.cos(np.deg2rad(lat2)),
                        np.cos(np.deg2rad(lat1)) * np.sin(np.deg2rad(lat2))
                        - np.sin(np.deg2rad(lat1))
                        * np.cos(np.deg2rad(lat2))
                        * np.cos(np.deg2rad(long2 - long1)),
                    )
                )
                + 360.0
            ),
            360.0,
        )
        return bearing  # type: ignore

    @staticmethod
    def cal_dest_given_dist_bearing(
        lat: array, long: array, bearing: array, dist: array
    ) -> tuple[array, array]:
        """
        Calculate the destination point(s) given start point(s), bearing(s) and
        distance(s)

        Parameters
        ----------
        lat : float[]
            Latitude of start point(s) [deg]
        long : float[]
            Longitude of start point(s) [deg]
        bearing : float[]
            Target bearing(s) [deg 0-360]
        dist : float[]
            Target distance(s) [km]

        Returns
        -------
        lat2 : float[]
            Latitude of destination(s) [deg]
        long2 : float[]
            Longitude of destination(s) [deg]

        Notes
        -----
        Using mean Earth radius 6371.009km for the WGS84 ellipsoid.
        https://www.movable-type.co.uk/scripts/latlong.html
        """
        lat2 = np.rad2deg(
            np.arcsin(
                np.sin(np.deg2rad(lat)) * np.cos(dist / 6371.009)
                + np.cos(np.deg2rad(lat))
                * np.sin(dist / 6371.009)
                * np.cos(np.deg2rad(bearing))
            )
        )
        long2 = long + np.rad2deg(
            np.arctan2(
                np.sin(np.deg2rad(bearing))
                * np.sin(dist / 6371.009)
                * np.cos(np.deg2rad(lat)),
                np.cos(dist / 6371.009)
                - np.sin(np.deg2rad(lat)) * np.sin(np.deg2rad(lat2)),
            )
        )
        return lat2, np.mod(long2 + 540.0, 360.0) - 180.0

    @staticmethod
    def cal_cross_track_dist(
        path_lat1: array,
        path_long1: array,
        path_lat2: array,
        path_long2: array,
        point_lat: array,
        point_long: array,
    ) -> array:
        """
        Calculate the cross track distance between point(s) along a great circle
        path.

        Parameters
        ----------
        path_lat1 : float
            Latitude of first point of great circle path [deg]
        path_long1 : float
            Longitude of first point of great circle path [deg]
        path_lat2 : float
            Latitude of second point of great circle path [deg]
        path_long2 : float
            Longitude of second point of great circle point [deg]
        point_lat : float[]
            Latitude of point(s) [deg]
        point_long : float[]
            Longitude of point(s) [deg]

        Returns
        -------
        float[]
            Cross track distance [km]

        Notes
        -----
        Cross track distance using mean Earth radius 6371.009km for the WGS84
        ellipsoid.
        https://www.movable-type.co.uk/scripts/latlong.html
        """
        distance_cross_track = (
            np.arcsin(
                np.sin(
                    Cal.cal_great_circle_dist(
                        path_lat1, path_long1, point_lat, point_long
                    )
                    / 6371.009
                )
            )
            * np.sin(
                np.deg2rad(
                    Cal.cal_great_circle_bearing(
                        path_lat1, path_lat2, point_lat, point_long
                    )
                    - Cal.cal_great_circle_bearing(
                        path_lat1, path_long1, path_lat2, path_long2
                    )
                )
            )
            * 6371.009
        )
        return distance_cross_track  # type: ignore

    @staticmethod
    def cal_angle_diff(current_angle: array, target_angle: array) -> array:
        """
        Calculate the difference of two angles
        (+ve clockwise, -ve anti-clockwise).

        Parameters
        ----------
        current_angle : float[]
            Current angle [deg]
        target_angle : float[]
            Target angle [deg]

        Returns
        -------
        float[]
            Angle difference [deg]
        """
        return np.mod(target_angle - current_angle + 180.0, 360.0) - 180.0
