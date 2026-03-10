from __future__ import annotations

import math
from typing import TYPE_CHECKING, Generic, TypeVar

from typing_extensions import NamedTuple

if TYPE_CHECKING:
    from . import types as t
    from .array_api import ArrayApiNamespace

G_0: t.GravitationalAcceleration[float] = 9.80665
"""Standard gravitational acceleration, sea level"""

RADIUS_EARTH_EQUATORIAL: t.LengthM[float] = 6_378_137.0
"""Semi-major axis, Earth, WGS84"""
RADIUS_EARTH_POLAR: t.LengthM[float] = 6_356_752.3
"""Semi-minor axis, Earth, WGS84"""
RADIUS_EARTH_MEAN: t.LengthM[float] = 6_371_008.7714
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
    lon0: t.AngleRad,
    lat0: t.AngleRad,
    lon1: t.AngleRad,
    lat1: t.AngleRad,
    *,
    xp: ArrayApiNamespace | None,
) -> t.LengthM:
    """
    Returns the [Haversine great circle distance](https://en.wikipedia.org/wiki/Haversine_formula)
    between two coordinates.
    """
    d_lon = lon1 - lon0
    d_lat = lat1 - lat0

    xpr = math if xp is None else xp
    a = (xpr.sin(d_lat / 2)) ** 2 + (
        xpr.cos(lat0) * xpr.cos(lat1) * xpr.sin(d_lon / 2)
    ) ** 2
    c = 2 * xpr.asin(xpr.sqrt(a))

    return RADIUS_EARTH_MEAN * c


def bearing(
    lon0: t.AngleRad,
    lat0: t.AngleRad,
    lon1: t.AngleRad,
    lat1: t.AngleRad,
    *,
    xp: ArrayApiNamespace | None,
) -> t.AngleRad:
    """
    Returns the initial bearing (from origin to destination) along a
    [great-circle](https://en.wikipedia.org/wiki/Great_circle).

    :return: initial bearing, radians, [$-\\pi$, $\\pi$], clockwise from north
    """
    d_lon = lon1 - lon0

    xpr = math if xp is None else xp
    y = xpr.sin(d_lon) * xpr.cos(lat1)
    x = xpr.cos(lat0) * xpr.sin(lat1) - (
        xpr.sin(lat0) * xpr.cos(lat1) * xpr.cos(d_lon)
    )

    return xpr.atan2(y, x)


#
# coordinate transformations
#


T = TypeVar("T")


class Point2D(NamedTuple, Generic[T]):
    """A point in 2D space"""

    x: T
    y: T


class Point3D(NamedTuple, Generic[T]):
    """A point in 3D space"""

    x: T
    y: T
    z: T


def lla_to_ecef(
    lon: t.AngleRad,
    lat: t.AngleRad,
    alt: t.GeometricAltitudeM,
    *,
    xp: ArrayApiNamespace | None,
) -> Point3D[t.LengthM]:
    """
    Converts geodetic coordinates to Earth-centered, Earth-fixed coordinates.
    Equivalent to `epsg:4979 +proj=cart +ellps=WGS84` in PROJ.

    :return: (x, y, z) coordinates
    """
    xpr = math if xp is None else xp
    v = RADIUS_EARTH_MEAN / xpr.sqrt(1 - E2 * xpr.sin(lat) * xpr.sin(lat))

    x = (v + alt) * xpr.cos(lat) * xpr.cos(lon)
    y = (v + alt) * xpr.cos(lat) * xpr.sin(lon)
    z = (v * (1 - E2) + alt) * xpr.sin(lat)

    return Point3D(x, y, z)


def ecef_to_enu(
    dx: t.DeltaLengthM,
    dy: t.DeltaLengthM,
    dz: t.DeltaLengthM,
    lon_ref: t.AngleRad,
    lat_ref: t.AngleRad,
    *,
    xp: ArrayApiNamespace | None,
) -> Point3D[t.LengthM]:
    """
    Converts Earth-centered, Earth-fixed coordinates
    (x, y, z with respect to a reference point)
    to East-North-Up coordinates.

    :return: (east, north, up) coordinates
    """
    xpr = math if xp is None else xp
    s_lat = xpr.sin(lat_ref)
    c_lat = xpr.cos(lat_ref)
    s_lon = xpr.sin(lon_ref)
    c_lon = xpr.cos(lon_ref)

    east = -s_lon * dx + c_lon * dy
    north = -s_lat * c_lon * dx - s_lat * s_lon * dy + c_lat * dz
    up = c_lat * c_lon * dx + c_lat * s_lon * dy + s_lat * dz

    return Point3D(east, north, up)
