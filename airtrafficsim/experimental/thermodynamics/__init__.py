from dataclasses import dataclass
from typing import Annotated, Generic

from ..quantity import (
    AdiabaticIndex,
    Density,
    GasConstant,
    MolarMass,
    SpecificGasConstant,
    SpeedOfSound,
    StaticPressure,
    StaticTemperature,
)
from ..types import Array, ArrayOrScalarT

R: Annotated[float, GasConstant("J mol⁻¹ K⁻¹")] = 8.31446261815324
"""Universal gas constant"""

M_DRY_AIR: Annotated[float, MolarMass("kg mol⁻¹")] = 0.028964917
R_SPECIFIC_DRY_AIR: Annotated[float, SpecificGasConstant("J kg⁻¹ K⁻¹")] = (
    287.052874
)
GAMMA_DRY_AIR: Annotated[float, AdiabaticIndex(None)] = 1.4


def specific_gas_constant(
    molar_mass: Annotated[ArrayOrScalarT, MolarMass("kg mol⁻¹")],
) -> Annotated[ArrayOrScalarT, SpecificGasConstant("J kg⁻¹ K⁻¹")]:
    return R / molar_mass


@dataclass(frozen=True)
class GasState(Generic[ArrayOrScalarT]):
    temperature: Annotated[ArrayOrScalarT, StaticTemperature("K")]
    pressure: Annotated[ArrayOrScalarT, StaticPressure("Pa")]

    def density(
        self,
        specific_gas_constant: Annotated[
            Array | float, SpecificGasConstant("J kg⁻¹ K⁻¹")
        ],
    ) -> Annotated[ArrayOrScalarT, Density("kg m⁻³")]:
        return density(self.temperature, self.pressure, specific_gas_constant)


def density(
    temperature: Annotated[Array | float, StaticTemperature("K")],
    pressure: Annotated[Array | float, StaticPressure("Pa")],
    specific_gas_constant: Annotated[
        Array | float, SpecificGasConstant("J kg⁻¹ K⁻¹")
    ],
) -> Annotated[Array | float, Density("kg m⁻³")]:
    """Density of a perfect gas"""
    return pressure / (specific_gas_constant * temperature)


def speed_of_sound(
    temperature: Annotated[Array | float, StaticTemperature("K")],
    adiabatic_index: Annotated[Array | float, AdiabaticIndex(None)],
    specific_gas_constant: Annotated[
        Array | float, SpecificGasConstant("J kg⁻¹ K⁻¹")
    ],
) -> Annotated[Array | float, SpeedOfSound("m s⁻¹")]:
    """Speed of sound for an ideal gas"""
    return (adiabatic_index * specific_gas_constant * temperature) ** 0.5
