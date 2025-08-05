from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import NamedTuple

if TYPE_CHECKING:
    from . import types as t

R: t.GasConstantJMolK[float] = 8.31446261815324
"""Universal gas constant"""

M_DRY_AIR: t.MolarMassKGMol[float] = 0.028964917
R_SPECIFIC_DRY_AIR: t.SpecificGasConstantJKGK[float] = 287.052874
GAMMA_DRY_AIR: t.RatioOfSpecificHeats[float] = 1.4


def specific_gas_constant(
    molar_mass: t.MolarMassKGMol,
) -> t.SpecificGasConstantJKGK:
    return R / molar_mass


class GasState(NamedTuple):
    temperature: t.StaticTemperatureK
    pressure: t.StaticPressurePA

    def density(
        self,
        specific_gas_constant: t.SpecificGasConstantJKGK,
    ) -> t.DensityKGM3:
        """Density, perfect gas"""
        return density(self.temperature, self.pressure, specific_gas_constant)


def density(
    temperature: t.StaticTemperatureK,
    pressure: t.StaticPressurePA,
    specific_gas_constant: t.SpecificGasConstantJKGK,
) -> t.DensityKGM3:
    """Density, perfect gas"""
    return pressure / (specific_gas_constant * temperature)


def speed_of_sound(
    temperature: t.StaticTemperatureK,
    adiabatic_index: t.RatioOfSpecificHeats,
    specific_gas_constant: t.SpecificGasConstantJKGK,
) -> t.SpeedOfSoundMPS:
    """Speed of sound, perfect gas"""
    return (adiabatic_index * specific_gas_constant * temperature) ** 0.5


def dynamic_pressure(
    rho: t.DensityKGM3,
    tas: t.TasMPS,
) -> t.DynamicPressurePA:
    """Dynamic pressure, incompressible flow"""
    return 0.5 * rho * tas**2


def total_pressure(
    tas: t.TasMPS,
    rho: t.DensityKGM3,
    p: t.StaticPressurePA,
    gamma: t.RatioOfSpecificHeats = GAMMA_DRY_AIR,
) -> t.TotalPressurePA:
    """Total pressure, compressible flow"""
    # NOTE: from bernoulli's formula
    inner = 1 + (gamma - 1) / (2 * gamma) * rho / p * tas**2
    return p * inner ** (gamma / (gamma - 1))


def total_pressure_behind_normal_shock(
    tas: t.TasMPS,
    rho: t.DensityKGM3,
    p: t.StaticPressurePA,
    gamma: t.RatioOfSpecificHeats = GAMMA_DRY_AIR,
) -> t.TotalPressurePA:
    """Total pressure, behind normal shock wave, supersonic flow"""
    common = rho / p * tas**2
    inner = ((gamma + 1) ** 2 / gamma * common) / (4 * common - 2 * (gamma - 1))
    return (1 + gamma) / (2 * gamma) * rho * tas**2 * inner ** (1 / (gamma - 1))


def impact_pressure(
    tas: t.TasMPS,
    rho: t.DensityKGM3,
    p: t.StaticPressurePA,
    gamma: t.RatioOfSpecificHeats = GAMMA_DRY_AIR,
) -> t.ImpactPressurePA:
    """Impact pressure, compressible flow"""
    return total_pressure(tas, rho, p, gamma) - p


def impact_pressure_behind_normal_shock(
    tas: t.TasMPS,
    a: t.SpeedOfSoundMPS,
    p: t.StaticPressurePA,
    gamma: t.RatioOfSpecificHeats = GAMMA_DRY_AIR,
) -> t.TotalPressurePA:
    """Impact pressure, behind normal shock wave, supersonic flow"""
    inner = (gamma + 1) ** 2 / (4 * gamma - 2 * (gamma - 1) * (a / tas) ** 2)
    return (
        (1 + gamma) / 2 * (tas / a) ** 2 * p * (inner ** (1 / (gamma - 1)) - 1)
    )
