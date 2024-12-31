from typing import Generic, NamedTuple

from typing_extensions import deprecated

from .types import ArrayOrFloat


@deprecated("[airtrafficsim.experimental.geospatial.point.Point2D][]")
class Point2D(NamedTuple, Generic[ArrayOrFloat]):
    """A coordinate in 2D."""

    lng: ArrayOrFloat
    """Longitude of the point(s) [rad]"""
    lat: ArrayOrFloat
    """Latitude of the point(s) [rad]"""
