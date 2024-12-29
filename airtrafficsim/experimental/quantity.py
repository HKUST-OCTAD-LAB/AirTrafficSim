"""
Markers for use in type annotations.

It is important to note that they **do not** store any data, but merely serve
as decoupled metadata for documentation.

For example:

```pycon
>>> from typing import Annotated
>>> from airtrafficsim.experimental.quantity import CAS, EAS
>>> def cas_to_eas(cas: Annotated[float, CAS]) -> Annotated[float, EAS]:
>>>     ...
```

The function here expects a plain `float`, not a wrapped `CAS` object.
At runtime, the types are effectively erased and static type checkers will
not catch incompatible quantities.
"""
# TODO: beartype integration

from dataclasses import dataclass
from typing import Generic, Literal, TypeAlias, TypeVar

Units = TypeVar("Units", bound=str | None)
"""
All possible units of measurements for a quantity.
When annotating a numerical value, the specific unit (SI or US customary)
should be specified.
"""


@dataclass(frozen=True)
class _Quantity(Generic[Units]):
    unit: Units


#
# Base
#

Length: TypeAlias = _Quantity[Literal["m", "ft"]]
Mass: TypeAlias = _Quantity[Literal["kg", "lbm"]]
Temperature: TypeAlias = _Quantity[Literal["K", "°C", "°F", "°R"]]
# Angle: TypeAlias = Dimension[Literal["rad", "deg"]]

#
# Derived
#

Force: TypeAlias = _Quantity[Literal["N", "lbf"]]
Pressure: TypeAlias = _Quantity[Literal["Pa", "psi"]]
Energy: TypeAlias = _Quantity[Literal["J"]]
Power: TypeAlias = _Quantity[Literal["W"]]
Speed: TypeAlias = _Quantity[Literal["m s⁻¹", "knots"]]
Acceleration: TypeAlias = _Quantity[Literal["m s⁻²", "ft s⁻²"]]
Density: TypeAlias = _Quantity[Literal["kg m⁻³", "slug ft⁻³"]]
GasConstant: TypeAlias = _Quantity[Literal["J mol⁻¹ K⁻¹"]]
MolarMass: TypeAlias = _Quantity[Literal["kg mol⁻¹"]]
SpecificGasConstant: TypeAlias = _Quantity[Literal["J kg⁻¹ K⁻¹"]]

#
# disambiguation
#


@dataclass(frozen=True)
class GeopotentialAltitude(Length):
    """Geopotential altitude above mean sea level"""


@dataclass(frozen=True)
class GeometricAltitude(Length):
    """Geometric altitude"""


@dataclass(frozen=True)
class StaticTemperature(Temperature):
    """Static temperature"""


@dataclass(frozen=True)
class DynamicTemperature(Temperature):
    """Dynamic temperature"""


@dataclass(frozen=True)
class TotalTemperature(Temperature):
    """Total temperature"""


@dataclass(frozen=True)
class StaticPressure(Pressure):
    """Static pressure"""


@dataclass(frozen=True)
class DynamicPressure(Pressure):
    """Dynamic pressure"""


@dataclass(frozen=True)
class TotalPressure(Pressure):
    """Total pressure"""


@dataclass(frozen=True)
class IAS(Speed):
    """Indicated airspeed"""


@dataclass(frozen=True)
class CAS(Speed):
    """Calibrated airspeed"""


@dataclass(frozen=True)
class EAS(Speed):
    """Equivalent airspeed"""


@dataclass(frozen=True)
class TAS(Speed):
    """True airspeed"""


@dataclass(frozen=True)
class GS(Speed):
    """Ground speed"""


@dataclass(frozen=True)
class WindSpeed(Speed):
    """Wind speed in the inertial reference frame"""


@dataclass(frozen=True)
class SpeedOfSound(Speed):
    """Speed of sound"""


@dataclass(frozen=True)
class GravitationalAcceleration(Acceleration):
    """Gravitational acceleration"""


@dataclass(frozen=True)
class TemperatureGradient(_Quantity[Literal["K m⁻¹"]]):
    """Lapse rate"""


@dataclass(frozen=True)
class MachNumber(_Quantity[None]):
    """Mach number"""


@dataclass(frozen=True)
class AdiabaticIndex(_Quantity[None]):
    """Ratio of specific heats, isentropic expansion factor"""


# no generic newtypes: https://github.com/python/mypy/issues/3331
@dataclass(frozen=True)
class Delta(Generic[Units]):
    """A difference between two quantities"""

    quantity: _Quantity[Units]
