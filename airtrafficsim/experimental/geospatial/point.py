from typing import Generic, NamedTuple, TypeVar

T = TypeVar("T")


class Point(NamedTuple, Generic[T]):
    x: T
    y: T


class Point3D(NamedTuple, Generic[T]):
    x: T
    y: T
    z: T
