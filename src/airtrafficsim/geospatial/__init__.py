from __future__ import annotations

from typing import TYPE_CHECKING

from .point import Point3D

if TYPE_CHECKING:
    from typing import Annotated

    from ..annotations import (
        Angle,
        Delta,
        GeometricAltitude,
        GravitationalAcceleration,
        Length,
    )
    from ..types import Array

G_0: Annotated[float, GravitationalAcceleration("m s⁻²")] = 9.80665
"""Standard gravitational acceleration, sea level"""

RADIUS_EARTH_EQUATORIAL: Annotated[float, Length("m")] = 6_378_137.0
"""Semi-major axis, Earth, WGS84"""
RADIUS_EARTH_POLAR: Annotated[float, Length("m")] = 6_356_752.3
"""Semi-minor axis, Earth, WGS84"""
RADIUS_EARTH_MEAN: Annotated[float, Length("m")] = 6_371_008.7714
"""Mean radius of semi-axes, Earth, WGS84"""

F_INV = 298.257223563
"""
Inverse flattening
$f = \\frac{R_\\text{equator} - R_\\text{pole}}{R_\\text{equator}}$
"""
F = 1 / F_INV
"""Flattening"""
E2 = 1 - (1 - F) * (1 - F)
"""Eccentricity, squared"""


def distance(
    lon0: Annotated[Array, Angle("rad")],
    lat0: Annotated[Array, Angle("rad")],
    lon1: Annotated[Array, Angle("rad")],
    lat1: Annotated[Array, Angle("rad")],
) -> Annotated[Array, Length("m")]:
    """
    Returns the [Haversine great circle distance](https://en.wikipedia.org/wiki/Haversine_formula)
    between two coordinates.
    """
    xp = lat0.__array_namespace__()
    d_lon = lon1 - lon0
    d_lat = lat1 - lat0

    a = xp.square(xp.sin(d_lat / 2)) + xp.square(
        xp.cos(lat0) * xp.cos(lat1) * xp.sin(d_lon / 2)
    )
    c = 2 * xp.arcsin(xp.sqrt(a))

    return RADIUS_EARTH_MEAN * c


def bearing(
    lon0: Annotated[Array, Angle("rad")],
    lat0: Annotated[Array, Angle("rad")],
    lon1: Annotated[Array, Angle("rad")],
    lat1: Annotated[Array, Angle("rad")],
) -> Annotated[Array, Angle("rad")]:
    """
    Returns the initial bearing (from origin to destination) along a
    [great-circle](https://en.wikipedia.org/wiki/Great_circle).

    :return: initial bearing, radians, [$-\\pi$, $\\pi$], clockwise from north
    """
    xp = lon0.__array_namespace__()
    d_lon = lon1 - lon0

    y = xp.sin(d_lon) * xp.cos(lat1)
    x = xp.cos(lat0) * xp.sin(lat1) - (
        xp.sin(lat0) * xp.cos(lat1) * xp.cos(d_lon)
    )

    return xp.arctan2(y, x)


#
# coordinate transformations
#


def lla_to_ecef(
    lon: Annotated[Array, Angle("rad")],
    lat: Annotated[Array, Angle("rad")],
    alt: Annotated[Array, GeometricAltitude("m")],
) -> Annotated[Point3D, Length("m")]:
    """
    Converts geodetic coordinates to Earth-centered, Earth-fixed coordinates.
    Equivalent to `epsg:4979 +proj=cart +ellps=WGS84` in PROJ.

    :return: (x, y, z) coordinates
    """
    xp = lon.__array_namespace__()
    v = RADIUS_EARTH_MEAN / xp.sqrt(1 - E2 * xp.sin(lat) * xp.sin(lat))

    x = (v + alt) * xp.cos(lat) * xp.cos(lon)
    y = (v + alt) * xp.cos(lat) * xp.sin(lon)
    z = (v * (1 - E2) + alt) * xp.sin(lat)

    return Point3D(x, y, z)


def ecef_to_enu(
    dx: Annotated[Array, Delta(Length("m"))],
    dy: Annotated[Array, Delta(Length("m"))],
    dz: Annotated[Array, Delta(Length("m"))],
    lon_ref: Annotated[Array, Angle("rad")],
    lat_ref: Annotated[Array, Angle("rad")],
) -> Annotated[Point3D, Length("m")]:
    """
    Converts Earth-centered, Earth-fixed coordinates
    (x, y, z with respect to a reference point)
    to East-North-Up coordinates.

    :return: (east, north, up) coordinates
    """
    xp = dx.__array_namespace__()
    s_lat = xp.sin(lat_ref)
    c_lat = xp.cos(lat_ref)
    s_lon = xp.sin(lon_ref)
    c_lon = xp.cos(lon_ref)

    east = -s_lon * dx + c_lon * dy
    north = -s_lat * c_lon * dx - s_lat * s_lon * dy + c_lat * dz
    up = c_lat * c_lon * dx + c_lat * s_lon * dy + s_lat * dz

    return Point3D(east, north, up)
