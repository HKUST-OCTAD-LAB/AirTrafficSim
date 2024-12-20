from typing import Generic, NamedTuple

from .types import ArrayOrFloat


# TODO(abrah): make this generic
class Point2D(NamedTuple, Generic[ArrayOrFloat]):
    """A coordinate in 2D."""

    lng: ArrayOrFloat
    """Longitude of the point(s) [rad]"""
    lat: ArrayOrFloat
    """Latitude of the point(s) [rad]"""
