"""
Implementation of the Base of aircraft data (BADA) Family 3.

Revision: 3.12 (No. 14/04/24-44)

See also:

- determination of air density (3.1-21)
[airtrafficsim.experimental.thermodynamics.density][]
- determination of speed of sound (3.1-22)
[airtrafficsim.experimental.thermodynamics.speed_of_sound][]
"""

import math
from typing import Annotated

from ..common import G_0  # 3.1.2
from ..quantity import (
    TAS,
    Delta,
    GeopotentialAltitude,
    MachNumber,
    SpeedOfSound,
    StaticPressure,
    StaticTemperature,
)
from ..thermodynamics import (
    GAMMA_DRY_AIR as KAPPA,  # 3.1.2
)
from ..thermodynamics import (
    R_SPECIFIC_DRY_AIR,  # 3.1.2
    GasState,
    speed_of_sound,
)
from ..types import Array, ArrayOrScalarT
from .isa import (
    BETA_BELOW_TROP,  # 3.1.2
    H_BELOW_TROP,  # 3.1-11
    P_0,  # 3.1.1
    P_11,  # 3.1-19
    # RHO_0,  # 3.1.1
    T_0,  # 3.1.1
    T_11,  # 3.1-14
)

A_0: Annotated[float, SpeedOfSound("m s⁻¹")] = 340.294  # 3.1.1

# NOTE: bada only considers <20km with two layers.
# for full coverage (at a cost of performance), use the full resolution ISA
# model instead (which uses np.searchsorted).


class BelowTropopause:
    """Marker to indicate the quantity is valid below the tropopause."""


class AboveTropopause:
    """Marker to indicate the quantity is valid above the tropopause."""


def temperature_below_tropopause(
    altitude: Annotated[Array | float, GeopotentialAltitude],
    delta_temperature: Annotated[
        Array | float, Delta(StaticTemperature("K"))
    ] = 0.0,
) -> Annotated[Array | float, StaticTemperature("K"), BelowTropopause]:
    """
    Temperature below the tropopause, lapsing linearly with altitude (3.1-13)
    """
    return T_0 + delta_temperature + altitude * BETA_BELOW_TROP


def temperature_above_tropopause(
    delta_temperature: Annotated[ArrayOrScalarT, Delta(StaticTemperature("K"))],
) -> Annotated[ArrayOrScalarT, StaticTemperature("K"), AboveTropopause]:
    """Temperature above the tropopause, isothermal (3.1-15, 3.1-16)."""
    return T_11 + delta_temperature


def pressure_below_tropopause(
    temperature_below_trop: Annotated[
        Array | float, StaticTemperature("K"), BelowTropopause
    ],
    delta_temperature: Annotated[
        Array | float, Delta(StaticTemperature("K"))
    ] = 0.0,
) -> Annotated[Array | float, StaticPressure("Pa"), BelowTropopause]:
    """Pressure below tropopause (3.1-18)"""
    return P_0 * (
        ((temperature_below_trop - delta_temperature) / T_0)
        ** (-G_0 / (R_SPECIFIC_DRY_AIR * BETA_BELOW_TROP))
    )


def pressure_above_tropopause(
    altitude: Annotated[ArrayOrScalarT, GeopotentialAltitude("m")],
) -> Annotated[ArrayOrScalarT, StaticPressure("Pa"), AboveTropopause]:
    """Pressure above tropopause (3.1-20)"""
    exp = (
        math.exp
        if isinstance(altitude, float)
        else altitude.__array_namespace__().exp  # type: ignore
    )
    return P_11 * (
        exp((altitude - H_BELOW_TROP) * (-G_0 / (R_SPECIFIC_DRY_AIR * T_11)))
    )


def atmosphere(
    altitude: Annotated[Array, GeopotentialAltitude("m")],
    delta_temperature: Annotated[Array, Delta(StaticTemperature("K"))],
) -> GasState[Array]:
    """
    BADA3 atmospheric model.

    Non-standard atmosphere conditions are modelled with the
    ISA temperature deviation.

    Note that this is only valid for 0-20km, unlike
    [airtrafficsim.experimental.performance.isa][].
    """
    xp = altitude.__array_namespace__()
    tropo_mask = altitude <= H_BELOW_TROP
    temperature = xp.where(
        tropo_mask,
        temperature_below_tropopause(altitude, delta_temperature),
        temperature_above_tropopause(delta_temperature),
    )
    return GasState(
        temperature=temperature,
        pressure=(
            xp.where(
                tropo_mask,
                pressure_below_tropopause(temperature, delta_temperature),
                pressure_above_tropopause(altitude),
            )
        ),
    )


def mach_number(
    tas: Annotated[Array | float, TAS("m s⁻¹")],
    temperature: Annotated[Array | float, StaticTemperature("K")],
) -> Annotated[Array | float, MachNumber(None)]:
    a = speed_of_sound(temperature, KAPPA, R_SPECIFIC_DRY_AIR)
    return tas / a
