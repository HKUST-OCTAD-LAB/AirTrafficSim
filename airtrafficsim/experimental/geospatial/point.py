from typing import Generic, NamedTuple, TypeVar

T = TypeVar("T")

# TODO: should we use inheritance to represent llh vs xyz?


class Point2D(NamedTuple, Generic[T]):
    """A point in 2D space"""

    x: T
    y: T


class Point3D(NamedTuple, Generic[T]):
    """A point in 3D space"""

    x: T
    y: T
    z: T
