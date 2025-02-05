"""
Context-specific metadata for types (PEP-593).

It is important to note that they **do not** store any data, but merely serve
as decoupled metadata for documentation.

For example:

```pycon
>>> from typing import Annotated
>>> from airtrafficsim.quantity import CAS, EAS
>>> import airtrafficsim.units as u
>>> def eas_from_cas(
...     cas: Annotated[float, CAS(u.MPS)]
... ) -> Annotated[float, EAS(u.MPS)]:
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
from typing import ClassVar, TypeAlias

from . import units as u

Unit: TypeAlias = u.UnitBase


@dataclass(frozen=True, slots=True)
class Quantity:
    """
    Base class for quantities with runtime unit validation.

    Subclasses can define `allowed_units: ClassVar[tuple[Unit, ...]]` to
    restrict the allowed units for instances of that subclass.
    If `allowed_units` is not defined, any Unit is allowed.
    """

    unit: Unit
    allowed_units: ClassVar[tuple[Unit | None, ...]] = ()

    def __post_init__(self) -> None:
        allowed = self.__class__.allowed_units
        if not len(allowed):
            # no restriction
            return
        if self.unit not in allowed:
            raise ValueError(
                f"invalid unit `{self.unit}` for `{self.__class__.__name__}`\n"
                f"help: allowed units: `{allowed}`"
            )

    def to_siunitx(self) -> str:
        return self.unit.to_siunitx()


#
# Base
#


class Time(Quantity):
    allowed_units = (u.SECOND, u.MINUTE, u.HOUR)


class Length(Quantity):
    allowed_units = (u.METER, u.FOOT, u.NMI, u.MILE)


class Mass(Quantity):
    allowed_units = (u.KILOGRAM, u.POUND)


class Temperature(Quantity):
    allowed_units = (u.KELVIN, u.CELSIUS, u.FAHRENHEIT, u.RANKINE)


class Angle(Quantity):
    allowed_units = (u.RAD, u.DEGREE)


#
# Derived
#


class Force(Quantity):
    allowed_units = (u.NEWTON, u.POUND_FORCE)


class Pressure(Quantity):
    allowed_units = (u.PASCAL, u.PSI, u.INHG)


class Energy(Quantity):
    allowed_units = (u.JOULE,)


class Power(Quantity):
    allowed_units = (u.WATT,)


class Velocity(Quantity):
    allowed_units = (u.MPS, u.KT, u.FPM, u.MPH, u.KPH)


class Acceleration(Quantity):
    allowed_units = (u.METER * u.SECOND**-2, u.FOOT * u.SECOND**-2)


class Density(Quantity):
    allowed_units = (u.KILOGRAM * u.METER**-3, u.SLUG * u.FOOT**-3)


class GasConstant(Quantity):
    allowed_units = (u.JOULE * u.MOLE**-1 * u.KELVIN**-1,)


class MolarMass(Quantity):
    allowed_units = (u.KILOGRAM * u.MOLE**-1,)


class SpecificGasConstant(Quantity):
    allowed_units = (u.JOULE * u.KILOGRAM**-1 * u.KELVIN**-1,)


class ThrustSpecificFuelConsumption(Quantity):
    allowed_units = (
        u.KILOGRAM * u.SECOND**-1 * u.NEWTON**-1,
        # u.GRAM * u.SECOND**-1 * (u.KILO * u.NEWTON) ** -1,
        u.POUND * u.HOUR**-1 * u.POUND_FORCE**-1,
    )


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


class TemperatureGradient(Quantity):
    """Lapse rate, below tropopause, ISA"""

    allowed_units = (u.KELVIN * u.METER**-1,)


class MachNumber(Quantity):
    """Mach number"""

    allowed_units = (None,)


class RatioOfSpecificHeats(Quantity):
    """Ratio of specific heats"""

    allowed_units = (None,)


#
# Newtype-like wrapper to indicate deltas
# see: https://github.com/python/mypy/issues/3331
#


@dataclass(frozen=True, slots=True)
class Delta:
    """A difference between two quantities"""

    quantity: Quantity
