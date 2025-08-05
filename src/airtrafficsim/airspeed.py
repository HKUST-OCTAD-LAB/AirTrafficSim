r"""
Implements common airspeed conversions.

```txt
        _________________
        v               v
IAS    CAS --> EAS <-> TAS    GS
            ^           |
            |           |------> q
            |           |
            |           |------> p_t ----> q_c
            |                               |
            |                               v
            |                    compressibility factor f
            |                               |
            |-------------------------------|
```

The equivalent airspeed $V_e$ is such that the dynamic pressure at some altitude
$q = \frac{1}{2} \rho V^2$ is the same as the dynamic pressure at
[sea level ISA conditions][airtrafficsim.performance.isa]
$q = \frac{1}{2} \rho_0 V_e^2$. EAS and TAS is related through
[airtrafficsim.performance.airspeed.eas_from_tas][].
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .constants import A_0, P_0, RHO_0
from .thermo import (
    GAMMA_DRY_AIR,
    impact_pressure,
    impact_pressure_behind_normal_shock,
)

if TYPE_CHECKING:
    from . import types as t


def impact_pressure_from_cas(
    cas: t.CasMPS,
    gamma: t.RatioOfSpecificHeats = GAMMA_DRY_AIR,
) -> t.ImpactPressurePA:
    """Impact pressure, compressible flow"""
    return impact_pressure(cas, RHO_0, P_0, gamma)


def impact_pressure_from_cas_behind_normal_shock(
    cas: t.CasMPS,
    gamma: t.RatioOfSpecificHeats = GAMMA_DRY_AIR,
) -> t.ImpactPressurePA:
    """Impact pressure, behind normal shock wave, supersonic flow"""
    return impact_pressure_behind_normal_shock(cas, A_0, P_0, gamma)


def density_factor(
    rho: t.DensityKGM3,
) -> t.DensityFactor:
    return (rho / RHO_0) ** 0.5


def eas_from_tas(
    tas: t.TasMPS,
    rho: t.DensityKGM3,
) -> t.EasMPS:
    """Converts TAS to EAS"""
    return tas * density_factor(rho)


def tas_from_eas(
    eas: t.EasMPS,
    rho: t.DensityKGM3,
) -> t.TasMPS:
    """Converts EAS to TAS"""
    return eas / density_factor(rho)


def compressibility_factor(
    qc: t.ImpactPressurePA,
    p: t.StaticPressurePA,
    gamma: t.RatioOfSpecificHeats = GAMMA_DRY_AIR,
) -> t.CompressibilityFactor:
    """Assumption: subsonic speeds"""
    exponent = (gamma - 1) / gamma
    inner = (qc / p + 1) ** exponent - 1
    return (exponent * p / qc * inner) ** 0.5


def eas_from_cas(
    cas: t.CasMPS,
    p: t.StaticPressurePA,
    gamma: t.RatioOfSpecificHeats = GAMMA_DRY_AIR,
) -> t.EasMPS:
    """Assumption: subsonic speeds"""
    qc = impact_pressure_from_cas(cas)
    f = compressibility_factor(qc, p, gamma)
    f0 = compressibility_factor(qc, P_0, gamma)
    return cas * f / f0


def tas_from_cas(
    cas: t.CasMPS,
    rho: t.DensityKGM3,
    p: t.StaticPressurePA,
) -> t.TasMPS:
    """Assumption: subsonic speeds"""
    eas = eas_from_cas(cas, p)
    return tas_from_eas(eas, rho)


def cas_from_tas(
    tas: t.TasMPS,
    rho: t.DensityKGM3,
    p: t.StaticPressurePA,
    gamma: t.RatioOfSpecificHeats = GAMMA_DRY_AIR,
) -> t.CasMPS:
    """Assumption: subsonic speeds"""
    eas = eas_from_tas(tas, rho)
    qc = impact_pressure(tas, rho, p, gamma)
    f = compressibility_factor(qc, p, gamma)
    f0 = compressibility_factor(qc, P_0, gamma)
    return eas * f0 / f
