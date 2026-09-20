import math

import pytest

import numpy as np
from airtrafficsim.geo import (
    RADIUS_EARTH_EQUATORIAL,
    RADIUS_EARTH_MEAN,
    RADIUS_EARTH_POLAR,
    Point3D,
    bearing,
    distance,
    ecef_to_enu,
    lla_to_ecef,
)

HKG = (math.radians(113.9185), math.radians(22.3080))
LHR = (math.radians(-0.4543), math.radians(51.4700))


def _distance_law_of_cosines(
    lon0: float, lat0: float, lon1: float, lat1: float
) -> float:
    return RADIUS_EARTH_MEAN * math.acos(
        math.sin(lat0) * math.sin(lat1)
        + math.cos(lat0) * math.cos(lat1) * math.cos(lon1 - lon0)
    )


@pytest.mark.parametrize(
    ("origin", "destination"),
    [
        (HKG, LHR),
        # same latitude away from the equator: `cos(lat)` terms matter
        ((0.0, math.radians(60)), (math.radians(90), math.radians(60))),
        # along the equator and along a meridian
        ((0.0, 0.0), (math.radians(90), 0.0)),
        ((0.0, 0.0), (0.0, math.radians(90))),
    ],
)
def test_distance(
    origin: tuple[float, float], destination: tuple[float, float]
) -> None:
    expected = _distance_law_of_cosines(*origin, *destination)
    assert distance(*origin, *destination, xp=None) == pytest.approx(expected)


def test_distance_known_value() -> None:
    assert distance(*HKG, *LHR, xp=None) == pytest.approx(9_630.7e3, rel=1e-4)


def test_distance_numpy_matches_python() -> None:
    lon1 = np.linspace(-np.pi, np.pi, 20)
    lat1 = np.linspace(-1.5, 1.5, 20)
    res = distance(HKG[0], HKG[1], lon1, lat1, xp=np)
    expected = [
        distance(HKG[0], HKG[1], float(lo), float(la), xp=None)
        for lo, la in zip(lon1, lat1)
    ]
    assert np.allclose(res, expected)


@pytest.mark.parametrize(
    ("destination", "expected"),
    [
        ((0.0, math.radians(10)), 0.0),  # north
        ((math.radians(10), 0.0), math.pi / 2),  # east
        ((0.0, math.radians(-10)), math.pi),  # south
        ((math.radians(-10), 0.0), -math.pi / 2),  # west
    ],
)
def test_bearing_cardinal(
    destination: tuple[float, float], expected: float
) -> None:
    assert bearing(0.0, 0.0, *destination, xp=None) == pytest.approx(expected)


def test_lla_to_ecef() -> None:
    """Reference values from `epsg:4979 +proj=cart +ellps=WGS84`."""
    x, y, z = lla_to_ecef(0.0, 0.0, 0.0, xp=None)
    assert (x, y, z) == pytest.approx((RADIUS_EARTH_EQUATORIAL, 0.0, 0.0))

    x, y, z = lla_to_ecef(0.0, math.pi / 2, 0.0, xp=None)
    assert (x, y, z) == pytest.approx((0.0, 0.0, RADIUS_EARTH_POLAR), abs=0.1)

    x, y, z = lla_to_ecef(0.0, math.radians(45), 0.0, xp=None)
    assert (x, y, z) == pytest.approx(
        (4_517_590.879, 0.0, 4_487_348.409), abs=1e-2
    )

    # altitude is measured along the ellipsoid normal
    x, y, z = lla_to_ecef(math.pi / 2, 0.0, 10_000.0, xp=None)
    assert (x, y, z) == pytest.approx(
        (0.0, RADIUS_EARTH_EQUATORIAL + 10_000.0, 0.0), abs=1e-6
    )


def _enu_from_hkg(d_lon: float, d_lat: float, alt: float) -> Point3D[float]:
    lon_ref, lat_ref = HKG
    ref = lla_to_ecef(lon_ref, lat_ref, 0.0, xp=None)
    p = lla_to_ecef(lon_ref + d_lon, lat_ref + d_lat, alt, xp=None)
    return ecef_to_enu(
        p.x - ref.x, p.y - ref.y, p.z - ref.z, lon_ref, lat_ref, xp=None
    )


def test_ecef_to_enu() -> None:
    # directly above the reference point
    enu = _enu_from_hkg(0.0, 0.0, 1_000.0)
    assert tuple(enu) == pytest.approx((0.0, 0.0, 1_000.0), abs=1e-6)

    # slightly north and slightly east of the reference point
    d = 1e-4
    enu = _enu_from_hkg(0.0, d, 0.0)
    assert enu.x == pytest.approx(0.0, abs=1e-6)
    assert enu.y > 600.0

    enu = _enu_from_hkg(d, 0.0, 0.0)
    assert enu.x > 500.0
    assert enu.y == pytest.approx(0.0, abs=0.1)
