"""
Context-specific metadata for types (PEP-593).

It is important to note that they **do not** store any data, but merely serve
as decoupled metadata for documentation.

For example:

```pycon
>>> from typing import Annotated
>>> from airtrafficsim.annotations import CAS, EAS
>>> def eas_from_cas(
...     cas: Annotated[float, CAS("m s⁻¹")]
... ) -> Annotated[float, EAS("m s⁻¹")]:
>>>     ...
```

The function here expects a plain `float`, not a wrapped `CAS` object.
At runtime, the types are effectively erased and static type checkers will
not catch incompatible quantities.
"""
# TODO: beartype integration
# TODO: add optional LaTeX protocol

from dataclasses import dataclass
from typing import Any, Generic, Literal, TypeAlias, TypeVar

Units = TypeVar("Units", bound=str | None)
"""
All possible units of measurements for a quantity.
When annotating a numerical value, the specific unit (SI or US customary)
should be specified.
"""


@dataclass(frozen=True, slots=True)
class _Quantity(Generic[Units]):
    unit: Units

    def __truediv__(self, other: "_Quantity[Any]") -> "Div":
        return Div(numerator=self, denominator=other)


#
# Base
#

Time: TypeAlias = _Quantity[Literal["s", "min", "hr"]]
Length: TypeAlias = _Quantity[Literal["m", "ft", "nmi", "mi"]]
Mass: TypeAlias = _Quantity[Literal["kg", "lbm"]]
Temperature: TypeAlias = _Quantity[Literal["K", "°C", "°F", "°R"]]
Angle: TypeAlias = _Quantity[Literal["rad", "deg"]]

#
# Derived
#

Force: TypeAlias = _Quantity[Literal["N", "lbf"]]
Pressure: TypeAlias = _Quantity[Literal["Pa", "psi", "hPa", "inHg"]]
Energy: TypeAlias = _Quantity[Literal["J"]]
Power: TypeAlias = _Quantity[Literal["W"]]
Velocity: TypeAlias = _Quantity[
    Literal["m s⁻¹", "kt", "ft min⁻¹", "mi hr⁻¹", "km hr⁻¹"]
]
Acceleration: TypeAlias = _Quantity[Literal["m s⁻²", "ft s⁻²"]]
Density: TypeAlias = _Quantity[Literal["kg m⁻³", "slug ft⁻³"]]
GasConstant: TypeAlias = _Quantity[Literal["J mol⁻¹ K⁻¹"]]
MolarMass: TypeAlias = _Quantity[Literal["kg mol⁻¹"]]
SpecificGasConstant: TypeAlias = _Quantity[Literal["J kg⁻¹ K⁻¹"]]
ThrustSpecificFuelConsumption: TypeAlias = _Quantity[
    Literal["kg s⁻¹ N⁻¹", "g s⁻¹ kN⁻¹", "lbm hr⁻¹ lbf⁻¹"]
]

#
# disambiguation
#


# ICAO definitions:
# - altitude: measured from the mean sea level (MSL)
# - height: measured from specific datum


class PressureAltitude(Length):
    """Pressure altitude, as measured from altimeter"""


class DensityAltitude(Length):
    """Density altitude, as measured from altimeter"""


class GeopotentialAltitude(Length):
    """Geopotential altitude, as measured from mean sea level"""


class GeometricAltitude(Length):
    """Geometric altitude, as measured from mean sea level"""


class GeodeticHeight(Length):
    """
    Geodetic height

    See: https://en.wikipedia.org/wiki/Geodetic_coordinates
    """


class StaticTemperature(Temperature):
    """Static temperature"""


class DynamicTemperature(Temperature):
    """Dynamic temperature"""


class TotalTemperature(Temperature):
    """Total temperature"""


class StaticPressure(Pressure):
    """Static pressure"""


class DynamicPressure(Pressure):
    """Dynamic pressure"""


class ImpactPressure(Pressure):
    """
    Impact pressure

    NOTE: For compressible flow, the measured impact pressure would be higher
    than the dynamic pressure
    """


class TotalPressure(Pressure):
    """Total pressure"""


class IAS(Velocity):
    """Indicated airspeed"""


class CAS(Velocity):
    """Calibrated airspeed"""


class EAS(Velocity):
    """Equivalent airspeed"""


class TAS(Velocity):
    """True airspeed"""


class GS(Velocity):
    """Ground speed"""


class WindSpeed(Velocity):
    """Wind speed in the inertial reference frame"""


class SpeedOfSound(Velocity):
    """Speed of sound"""


class GravitationalAcceleration(Acceleration):
    """Gravitational acceleration"""


class TemperatureGradient(_Quantity[Literal["K m⁻¹"]]):
    """Lapse rate, below tropopause, ISA"""


class MachNumber(_Quantity[None]):
    """Mach number"""


class AdiabaticIndex(_Quantity[None]):
    """Ratio of specific heats, isentropic expansion factor"""


#
# Newtype-like wrapper to indicate deltas
# see: https://github.com/python/mypy/issues/3331
#


@dataclass(frozen=True, slots=True)
class Delta(Generic[Units]):
    """A difference between two quantities"""

    quantity: _Quantity[Units]


@dataclass(frozen=True, slots=True)
class Div:
    """
    A ratio between two quantities.

    Used in [unit conversion][airtrafficsim.unit_conversion].
    """

    numerator: _Quantity[Any]
    denominator: _Quantity[Any]
