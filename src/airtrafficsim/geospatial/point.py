from typing import Generic, TypeVar

from typing_extensions import NamedTuple

from ..types import Array

T = TypeVar("T", bound=Array)


class Point2D(NamedTuple, Generic[T]):
    """A point in 2D space"""

    x: T
    y: T


class Point3D(NamedTuple, Generic[T]):
    """A point in 3D space"""

    x: T
    y: T
    z: T
