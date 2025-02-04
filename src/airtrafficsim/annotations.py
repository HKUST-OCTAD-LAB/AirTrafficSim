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
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Literal, TypeAlias, TypeVar

Units = TypeVar("Units", bound=str | None)
"""
All possible units of measurements for a quantity.
When annotating a numerical value, the specific unit (SI or US customary)
should be specified.
"""


@dataclass(frozen=True, slots=True)
class Quantity(Generic[Units]):
    unit: Units  # keeping it as a string for simplicity.

    def __truediv__(self, other: Quantity[Any]) -> Div:
        return Div(numerator=self, denominator=other)


#
# Base
#

Time: TypeAlias = Quantity[Literal["s", "min", "hr"]]
Length: TypeAlias = Quantity[Literal["m", "ft", "nmi", "mi"]]
Mass: TypeAlias = Quantity[Literal["kg", "lbm"]]
Temperature: TypeAlias = Quantity[Literal["K", "°C", "°F", "°R"]]
Angle: TypeAlias = Quantity[Literal["rad", "deg"]]

#
# Derived
#

Force: TypeAlias = Quantity[Literal["N", "lbf"]]
Pressure: TypeAlias = Quantity[Literal["Pa", "psi", "hPa", "inHg"]]
Energy: TypeAlias = Quantity[Literal["J"]]
Power: TypeAlias = Quantity[Literal["W"]]
Velocity: TypeAlias = Quantity[
    Literal["m s⁻¹", "kt", "ft min⁻¹", "mi hr⁻¹", "km hr⁻¹"]
]
Acceleration: TypeAlias = Quantity[Literal["m s⁻²", "ft s⁻²"]]
Density: TypeAlias = Quantity[Literal["kg m⁻³", "slug ft⁻³"]]
GasConstant: TypeAlias = Quantity[Literal["J mol⁻¹ K⁻¹"]]
MolarMass: TypeAlias = Quantity[Literal["kg mol⁻¹"]]
SpecificGasConstant: TypeAlias = Quantity[Literal["J kg⁻¹ K⁻¹"]]
ThrustSpecificFuelConsumption: TypeAlias = Quantity[
    Literal["kg s⁻¹ N⁻¹", "g s⁻¹ kN⁻¹", "lbm hr⁻¹ lbf⁻¹"]
]

#
# disambiguation
#


# ICAO definitions:
# - altitude: measured from the mean sea level (MSL)
# - height: measured from specific datum


class PressureAltitude(Length):
    """Pressure altitude, as measured by altimeter"""


class DensityAltitude(Length):
    """Density altitude, as measured by altimeter"""


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
    """Wind speed, inertial reference frame"""


class SpeedOfSound(Velocity):
    """Speed of sound"""


class GravitationalAcceleration(Acceleration):
    """Gravitational acceleration"""


class TemperatureGradient(Quantity[Literal["K m⁻¹"]]):
    """Lapse rate, below tropopause, ISA"""


class MachNumber(Quantity[None]):
    """Mach number"""


class RatioOfSpecificHeats(Quantity[None]):
    """Ratio of specific heats"""


#
# Newtype-like wrapper to indicate deltas
# see: https://github.com/python/mypy/issues/3331
#


@dataclass(frozen=True, slots=True)
class Delta(Generic[Units]):
    """A difference between two quantities"""

    quantity: Quantity[Units]


@dataclass(frozen=True, slots=True)
class Div:
    """
    A ratio between two quantities.

    Used in [unit conversion][airtrafficsim.unit_conversion].
    """

    numerator: Quantity[Any]
    denominator: Quantity[Any]
