"""
Implementation of the Base of aircraft data (BADA) Family 3.

Revision: 3.12 (No. 14/04/24-44)

Contents:

- [ ] 3 Operational Performance Models
    - [x] 3.1 Atmosphere Model
    - [ ] 3.2 Total-Energy Model
    - [ ] 3.3 Aircraft Type
    - [ ] 3.4 Mass
    - [ ] 3.5 Flight Envelope
    - [ ] 3.6 Aerodynamics
    - [ ] 3.7 Engine Thrust
    - [ ] 3.8 Reduced Climb Power
    - [ ] 3.9 Fuel Consumption
    - [ ] 3.10 Ground Movement
    - [ ] 3.11 Summary of Operations Performance Parameters
- [ ] 4 Airline Procedure Models
- [ ] 5 Global Aircraft Parameters
- [ ] 6 File Structure
    - [ ] 6.1 File Types
    - [ ] 6.2 File Configuration Management
    - [ ] 6.3 `Synonym` File Format
    - [ ] 6.4 `OPF` File Format
    - [ ] 6.5 `APF` File Format
    - [ ] 6.6 `PTF` File Format
    - [ ] 6.7 `PTD` File Format
    - [ ] 6.8 `BADA.GPF` File Format

The following functions are defined elsewhere:

- 3.1-21 Determination of air density
[airtrafficsim.thermodynamics.density][]
- 3.1-22 Determination of speed of sound
[airtrafficsim.thermodynamics.speed_of_sound][]
- 3.1-23, 3.1-24 CAS/TAS conversion
    - [airtrafficsim.performance.airspeed.tas_from_cas][]
    - [airtrafficsim.performance.airspeed.cas_from_tas][]
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from ..geospatial import G_0  # 3.1.2
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
    # A_0,  # 3.1.1
    BETA_BELOW_TROP,  # 3.1.2
    H_BELOW_TROP,  # 3.1-11
    P_0,  # 3.1.1
    P_11,  # 3.1-19
    # RHO_0,  # 3.1.1
    T_0,  # 3.1.1
    T_11,  # 3.1-14
)

if TYPE_CHECKING:
    from typing import Annotated

    from ..annotations import (
        TAS,
        Delta,
        GeopotentialAltitude,
        MachNumber,
        StaticPressure,
        StaticTemperature,
    )

    class BelowTropopause:
        """Marker to indicate the quantity is valid below the tropopause."""

    class AboveTropopause:
        """Marker to indicate the quantity is valid above the tropopause."""

#
# 3. Operational Performance Models
#
# BADA atmosphere only considers <20km with two layers: gradient and isothermal.
# for full coverage (at a cost of performance), use the full resolution ISA
# model instead (which uses np.searchsorted).
#


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
    [airtrafficsim.performance.isa][].
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
    """Mach/TAS conversion (3.1-26)"""
    a = speed_of_sound(temperature, KAPPA, R_SPECIFIC_DRY_AIR)
    return tas / a
