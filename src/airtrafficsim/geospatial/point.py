from typing import NamedTuple

from ..types import Array


# NOTE: generic namedtuple not supported in py<3.10
class Point2D(NamedTuple):
    """A point in 2D space"""

    x: Array
    y: Array


class Point3D(NamedTuple):
    """A point in 3D space"""

    x: Array
    y: Array
    z: Array
