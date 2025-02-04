from __future__ import annotations

from typing import TYPE_CHECKING, Generic, NamedTuple

from ..types import ArrayOrScalarT

if TYPE_CHECKING:
    from typing import Annotated

    from ..annotations import (
        TAS,
        Density,
        DynamicPressure,
        GasConstant,
        ImpactPressure,
        MolarMass,
        RatioOfSpecificHeats,
        SpecificGasConstant,
        SpeedOfSound,
        StaticPressure,
        StaticTemperature,
        TotalPressure,
    )
    from ..types import Array

R: Annotated[float, GasConstant("J mol⁻¹ K⁻¹")] = 8.31446261815324
"""Universal gas constant"""

M_DRY_AIR: Annotated[float, MolarMass("kg mol⁻¹")] = 0.028964917
R_SPECIFIC_DRY_AIR: Annotated[float, SpecificGasConstant("J kg⁻¹ K⁻¹")] = (
    287.052874
)
GAMMA_DRY_AIR: Annotated[float, RatioOfSpecificHeats(None)] = 1.4


def specific_gas_constant(
    molar_mass: Annotated[ArrayOrScalarT, MolarMass("kg mol⁻¹")],
) -> Annotated[ArrayOrScalarT, SpecificGasConstant("J kg⁻¹ K⁻¹")]:
    return R / molar_mass


class GasState(NamedTuple, Generic[ArrayOrScalarT]):
    temperature: Annotated[ArrayOrScalarT, StaticTemperature("K")]
    pressure: Annotated[ArrayOrScalarT, StaticPressure("Pa")]

    def density(
        self,
        specific_gas_constant: Annotated[
            Array | float, SpecificGasConstant("J kg⁻¹ K⁻¹")
        ],
    ) -> Annotated[ArrayOrScalarT, Density("kg m⁻³")]:
        """Density, perfect gas"""
        return density(self.temperature, self.pressure, specific_gas_constant)


def density(
    temperature: Annotated[Array | float, StaticTemperature("K")],
    pressure: Annotated[Array | float, StaticPressure("Pa")],
    specific_gas_constant: Annotated[
        Array | float, SpecificGasConstant("J kg⁻¹ K⁻¹")
    ],
) -> Annotated[Array | float, Density("kg m⁻³")]:
    """Density, perfect gas"""
    return pressure / (specific_gas_constant * temperature)


def speed_of_sound(
    temperature: Annotated[Array | float, StaticTemperature("K")],
    adiabatic_index: Annotated[Array | float, RatioOfSpecificHeats(None)],
    specific_gas_constant: Annotated[
        Array | float, SpecificGasConstant("J kg⁻¹ K⁻¹")
    ],
) -> Annotated[Array | float, SpeedOfSound("m s⁻¹")]:
    """Speed of sound, perfect gas"""
    return (adiabatic_index * specific_gas_constant * temperature) ** 0.5


def dynamic_pressure(
    rho: Annotated[Array | float, Density("kg m⁻³")],
    tas: Annotated[Array | float, TAS("m s⁻¹")],
) -> Annotated[Array | float, DynamicPressure("Pa")]:
    """Dynamic pressure, incompressible flow"""
    return 0.5 * rho * tas**2


def total_pressure(
    tas: Annotated[Array | float, TAS("m s⁻¹")],
    rho: Annotated[Array | float, Density("kg m⁻³")],
    p: Annotated[Array | float, StaticPressure("Pa")],
    gamma: Annotated[Array | float, RatioOfSpecificHeats(None)] = GAMMA_DRY_AIR,
) -> Annotated[Array | float, TotalPressure("Pa")]:
    """Total pressure, compressible flow"""
    # NOTE: from bernoulli's formula
    inner = 1 + (gamma - 1) / (2 * gamma) * rho / p * tas**2
    return p * inner ** (gamma / (gamma - 1))


def total_pressure_behind_normal_shock(
    tas: Annotated[Array | float, TAS("m s⁻¹")],
    rho: Annotated[Array | float, Density("kg m⁻³")],
    p: Annotated[Array | float, StaticPressure("Pa")],
    gamma: Annotated[Array | float, RatioOfSpecificHeats(None)] = GAMMA_DRY_AIR,
) -> Annotated[Array | float, TotalPressure("Pa")]:
    """Total pressure, behind normal shock wave, supersonic flow"""
    common = rho / p * tas**2
    inner = ((gamma + 1) ** 2 / gamma * common) / (4 * common - 2 * (gamma - 1))
    return (1 + gamma) / (2 * gamma) * rho * tas**2 * inner ** (1 / (gamma - 1))


def impact_pressure(
    tas: Annotated[Array, TAS("m s⁻¹")],
    rho: Annotated[Array, Density("kg m⁻³")],
    p: Annotated[Array, StaticPressure("Pa")],
    gamma: Annotated[Array, RatioOfSpecificHeats(None)] = GAMMA_DRY_AIR,
) -> Annotated[Array, ImpactPressure("Pa")]:
    """Impact pressure, compressible flow"""
    return total_pressure(tas, rho, p, gamma) - p


def impact_pressure_behind_normal_shock(
    tas: Annotated[Array | float, TAS("m s⁻¹")],
    a: Annotated[Array | float, SpeedOfSound("m s⁻¹")],
    p: Annotated[Array | float, StaticPressure("Pa")],
    gamma: Annotated[Array | float, RatioOfSpecificHeats(None)] = GAMMA_DRY_AIR,
) -> Annotated[Array | float, TotalPressure("Pa")]:
    """Impact pressure, behind normal shock wave, supersonic flow"""
    inner = (gamma + 1) ** 2 / (4 * gamma - 2 * (gamma - 1) * (a / tas) ** 2)
    return (
        (1 + gamma) / 2 * (tas / a) ** 2 * p * (inner ** (1 / (gamma - 1)) - 1)
    )
