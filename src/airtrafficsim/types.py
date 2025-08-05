"""This module contains a set of type aliases for `isqx` physical quantity kinds
and units.

Note that while static typing is usually a good idea, many core numerical parts
of the library (whose inputs and outputs are arrays) will **not** use static
typing.

This may be surprising: why not annotate `NDArray[np.float64] | float` and
`TypeVars`? We wish to suppose a wide range of numerical libraries, and
restricting ourselves to `numpy` will lead to many false positives in mypy
strict mode. See:

- https://docs.jax.dev/en/latest/jep/12049-type-annotations.html

Instead, we will utilise **unconstrained generic types** to signal to the
static checker that we want an `Unknown` type, not the `Any` type.

We will adopt the [array API](https://data-apis.org/array-api/latest)
for most computations, see:

- https://github.com/data-apis/array-api/issues/229
- https://github.com/data-apis/array-api/discussions/863
- https://github.com/data-apis/array-api-typing
"""

from __future__ import annotations

from typing import Annotated, TypeVar

import isqx
from isqx import aerospace as aero

_T = TypeVar("_T")

#
# custom quantity kinds and metadata objects
#

TEMPERATURE_GRADIENT = isqx.QtyKind(
    isqx.K * isqx.M**-1, ("temperature_gradient",)
)
"""Temperature lapse rate, e.g., in an atmosphere model."""

BelowTropopause = "below_tropopause"
STATIC_TEMPERATURE_BELOW_TROPO = aero.STATIC_TEMPERATURE[BelowTropopause]
STATIC_PRESSURE_BELOW_TROPO = isqx.STATIC_PRESSURE[BelowTropopause]

DENSITY_FACTOR = isqx.Dimensionless("density_factor")
COMPRESSIBILITY_FACTOR = isqx.Dimensionless("compressibility_factor")

#
# Type Aliases
#

# base
LengthM = Annotated[_T, isqx.LENGTH(isqx.M)]
AngleRad = Annotated[_T, isqx.ANGLE(isqx.RAD)]
GravitationalAcceleration = Annotated[
    _T, isqx.ACCELERATION_OF_FREE_FALL(isqx.M_PERS2)
]

# thermodynamics
PressurePA = Annotated[_T, isqx.PRESSURE(isqx.PA)]
PressureHPA = Annotated[_T, isqx.PRESSURE(isqx.HECTO * isqx.PA)]
DensityKGM3 = Annotated[_T, isqx.DENSITY(isqx.KG * isqx.M**-3)]

StaticTemperatureK = Annotated[_T, aero.STATIC_TEMPERATURE(isqx.K)]
StaticPressurePA = Annotated[_T, isqx.STATIC_PRESSURE(isqx.PA)]
DynamicPressurePA = Annotated[_T, isqx.DYNAMIC_PRESSURE(isqx.PA)]
ImpactPressurePA = Annotated[_T, aero.IMPACT_PRESSURE(isqx.PA)]
TotalPressurePA = Annotated[_T, aero.TOTAL_PRESSURE(isqx.PA)]

GasConstantJMolK = Annotated[
    _T, isqx.MOLAR_GAS_CONSTANT(isqx.J * isqx.MOL**-1 * isqx.K**-1)
]
MolarMassKGMol = Annotated[_T, isqx.MOLAR_MASS(isqx.KG * isqx.MOL**-1)]
SpecificGasConstantJKGK = Annotated[
    _T, isqx.SPECIFIC_GAS_CONSTANT(isqx.J * isqx.KG**-1 * isqx.K**-1)
]
TemperatureGradientKPM = Annotated[
    _T, TEMPERATURE_GRADIENT(isqx.K * isqx.M**-1)
]
StaticTemperatureKBelowTropo = Annotated[
    _T, STATIC_TEMPERATURE_BELOW_TROPO(isqx.K)
]
StaticPressurePABelowTropo = Annotated[_T, STATIC_PRESSURE_BELOW_TROPO(isqx.PA)]

# aerospace
CasMPS = Annotated[_T, aero.CAS(isqx.M_PERS)]
EasMPS = Annotated[_T, aero.EAS(isqx.M_PERS)]
TasMPS = Annotated[_T, aero.TAS(isqx.M_PERS)]
SpeedOfSoundMPS = Annotated[_T, isqx.SPEED_OF_SOUND(isqx.M_PERS)]

GeopotentialAltitudeM = Annotated[_T, aero.GEOPOTENTIAL_ALTITUDE(isqx.M)]
GeometricAltitudeM = Annotated[_T, aero.GEOMETRIC_ALTITUDE(isqx.M)]

# dimensionless
MachNumber = Annotated[_T, isqx.MACH_NUMBER]
RatioOfSpecificHeats = Annotated[_T, isqx.HEAT_CAPACITY_RATIO]
DensityFactor = Annotated[_T, DENSITY_FACTOR]
CompressibilityFactor = Annotated[_T, COMPRESSIBILITY_FACTOR]

# deltas
DeltaTemperatureK = Annotated[_T, isqx.TEMPERATURE[isqx.DELTA](isqx.K)]
DeltaLengthM = Annotated[_T, isqx.LENGTH[isqx.DELTA](isqx.M)]
