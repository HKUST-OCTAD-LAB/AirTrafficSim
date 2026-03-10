"""Utilities for turbofan.

- Bartel and Young, "Simplified Thrust and Fuel Consumption Models for Modern
  Two-Shaft Turbofan Engines", <https://doi.org/10.2514/1.35589>
"""

from __future__ import annotations

import math
from enum import Enum
from typing import TYPE_CHECKING, Annotated, Generic, NamedTuple, TypeVar

import isqx
import isqx.aerospace as aero
import isqx.usc

from .array_api import ArrayApiNamespace, linear_interp, where

if TYPE_CHECKING:
    from . import types as t


lb_to_kg = isqx.convert(isqx.usc.LB, isqx.KG)
m_to_in = isqx.convert(isqx.M, isqx.usc.IN)
nsperkg_to_lbfsperlb = isqx.convert(
    (isqx.N * isqx.S) / isqx.KG,
    (isqx.usc.LBF * isqx.S) / isqx.usc.LB,
)

SPECIFIC_THRUST = isqx.QtyKind(
    (isqx.N * isqx.S) / isqx.KG,
    ("specific_thrust",),
)

ExponentN = Annotated[t._T, isqx.Dimensionless("bartelyoung2008_exponent_n")]
ThrustFactorZ = Annotated[t._T, isqx.Dimensionless("bartelyoung2008_factor_z")]
BleedFractionCoreFlow = Annotated[
    t._T, isqx.Dimensionless("bleed_fraction_core_flow")
]
"""Customer bleed fraction from the HP compressor core flow.

For cabin pressurisation and anti-ice, bleed air is extracted instead of passing
through the full core. '0.04' means 4% of core flow.
"""
BleedInterceptFactor = Annotated[
    t._T, isqx.Dimensionless("bleed_intercept_factor")
]
"""Empirical parameter `A` from Eq. (8) / Fig. 9.

Vertical shift of the takeoff thrust-ratio curve caused by bleed extraction at
sea-level takeoff conditions, not itself a bleed fraction.
"""
GasGeneratorFunction = Annotated[
    t._T, isqx.Dimensionless("gas_generator_function")
]  # see Torenbeek
TsfcRatio = Annotated[
    t._T,
    isqx.ratio(
        aero.THRUST_SPECIFIC_FUEL_CONSUMPTION.si_coherent(),
        aero.THRUST_SPECIFIC_FUEL_CONSUMPTION["ref"].si_coherent(),
    ),
]
CasRatio = Annotated[
    t._T,
    isqx.ratio(
        aero.CALIBRATED_AIRSPEED.si_coherent(),
        aero.CALIBRATED_AIRSPEED["ref"].si_coherent(),
    ),
]
MachRatio = Annotated[
    t._T, isqx.ratio(isqx.MACH_NUMBER, isqx.MACH_NUMBER["ref"])
]
TakeoffAltitudePressureRatio = Annotated[
    t._T, isqx.Dimensionless("ambient_to_sls_pressure_ratio")
]
r"""Ambient static pressure divided by sea-level static ambient pressure.

This is the $p_{\mathrm{amb}} / p_{\mathrm{amb0}}$ input used by Eqs. (12-14).
"""
PressureRatioTo30kFt = Annotated[
    t._T, isqx.Dimensionless("ambient_to_30kft_pressure_ratio")
]
r"""Ambient static pressure divided by the 30,000 ft ISA reference pressure.

This is the $p_{\mathrm{amb}} / p_{\mathrm{amb30}}$ input used by
Eqs. (15), (17), and (19).
"""
HpCompressorWorkFraction = Annotated[
    t._T,
    isqx.Dimensionless("hp_compressor_work_fraction"),
]
"""Normalized Fig. 9 HP-compressor work coordinate in $[0, 1]$.

The paper only provides this graphically. The caller must provide the normalised
coordinate corresponding to the chart extraction.
"""
RefSpecificThrust = Annotated[
    t._T, SPECIFIC_THRUST((isqx.N * isqx.S) / isqx.KG)
]
"""Reference specific thrust $F^*/W_1^*$.

$F^*$ is net thrust at the aircraft's optimum-$L/D$ cruise condition.
`W_1^*` is engine inlet mass flow at that same condition.
The paper quotes this in lbf·s/lb.
"""
TakeoffAltitudeInterceptFactor = Annotated[
    t._T, isqx.Dimensionless("takeoff_altitude_intercept_factor")
]
TakeoffAltitudeLinearMachFactor = Annotated[
    t._T, isqx.Dimensionless("takeoff_altitude_linear_mach_factor")
]
TakeoffAltitudeQuadraticMachFactor = Annotated[
    t._T, isqx.Dimensionless("takeoff_altitude_quadratic_mach_factor")
]

_TValue = TypeVar("_TValue")


class QuadraticCoefficients(NamedTuple, Generic[_TValue]):
    """Quadratic fit coefficients for the manually extracted Fig. 9 curves."""

    c1: _TValue
    c2: _TValue
    c3: _TValue


#
# bartel and young (2008)
#


class ClimbRate(str, Enum):
    """Discrete climb-rate settings used by Tables 3 and 4."""

    FAST = "fast"
    MODERATE = "moderate"
    SLOW = "slow"


TABLE_2_MACH_RATIOS = (0.85, 0.92, 1.0, 1.08, 1.15)
TABLE_2_D = (0.73, 0.69, 0.66, 0.63, 0.60)
TABLE_4_CAS_RATIOS = (0.67, 0.75, 0.83, 0.92, 1.0)
TABLE_4_M = {
    ClimbRate.FAST: (0.40, 0.39, 0.38, 0.37, 0.36),
    ClimbRate.MODERATE: (0.39, 0.38, 0.37, 0.36, 0.35),
    ClimbRate.SLOW: (0.34, 0.33, 0.32, 0.31, 0.30),
}
TABLE_3_N = {
    ClimbRate.FAST: 0.97,
    ClimbRate.MODERATE: 0.93,
    ClimbRate.SLOW: 0.89,
}


def gas_generator_function_from_bypass_ratio(
    bypass_ratio: t.BypassRatio,
) -> GasGeneratorFunction:
    """Fig. 5 fit at sea-level static conditions."""
    return 0.06 * bypass_ratio + 0.64


BLEED_FRACTIONS = (0.0, 0.02, 0.04, 0.06, 0.08)
BLEED_A_C1 = (1.0, 0.966328, 0.929699, 0.895747, 0.859206)
BLEED_A_C2 = (0.0, -0.035753, -0.0688748, -0.101663, -0.139769)
BLEED_A_C3 = (0.0, 0.0158028, 0.0302575, 0.0446968, 0.0667068)


def bleed_intercept_coefficients(
    bleed_fraction_core_flow: BleedFractionCoreFlow,
    *,
    xp: ArrayApiNamespace | None,
) -> QuadraticCoefficients:
    """Fig. 9 coefficients, linearly interpolated in bleed fraction.

    The 0%, 2%, 4%, 6%, and 8% curves were manually extracted from the paper.
    Values outside that range are clamped by `xp.interp` to the nearest edge.
    """
    return QuadraticCoefficients(
        linear_interp(
            bleed_fraction_core_flow, BLEED_FRACTIONS, BLEED_A_C1, xp=xp
        ),
        linear_interp(
            bleed_fraction_core_flow, BLEED_FRACTIONS, BLEED_A_C2, xp=xp
        ),
        linear_interp(
            bleed_fraction_core_flow, BLEED_FRACTIONS, BLEED_A_C3, xp=xp
        ),
    )


def bleed_intercept_factor(
    hp_compressor_work_fraction: HpCompressorWorkFraction,
    bleed_fraction_core_flow: BleedFractionCoreFlow,
    *,
    xp: ArrayApiNamespace | None,
) -> BleedInterceptFactor:
    """Fig. 9 fit for the bleed-induced intercept parameter `A`.

    The paper does not provide a combined altitude-plus-bleed law, so this
    factor should not be folded into Eq. (11).
    """
    coeffs = bleed_intercept_coefficients(bleed_fraction_core_flow, xp=xp)
    return (
        coeffs.c1
        + coeffs.c2 * hp_compressor_work_fraction
        + coeffs.c3 * (hp_compressor_work_fraction**2)
    )


def takeoff_thrust_ratio_with_bleed(
    mach: t.MachNumber,
    bypass_ratio: t.BypassRatio,
    gas_generator_function: GasGeneratorFunction,
    hp_compressor_work_fraction: HpCompressorWorkFraction,
    bleed_fraction_core_flow: BleedFractionCoreFlow,
    *,
    xp: ArrayApiNamespace | None,
) -> ExponentN:
    """Sea-level takeoff thrust ratio with customer bleed.

    This implements Eq. (8) with the Fig. 9 fit supplying parameter `A`.
    The paper does not define how to combine this bleed correction with the
    altitude law of Eq. (11), so this helper is sea-level only.
    """
    return takeoff_thrust_ratio_polynomial(
        mach,
        bypass_ratio,
        gas_generator_function,
        intercept_factor=bleed_intercept_factor(
            hp_compressor_work_fraction, bleed_fraction_core_flow, xp=xp
        ),
    )


def takeoff_thrust_with_bleed(
    reference_thrust: t.ThrustN,
    mach: t.MachNumber,
    bypass_ratio: t.BypassRatio,
    gas_generator_function: GasGeneratorFunction,
    hp_compressor_work_fraction: HpCompressorWorkFraction,
    bleed_fraction_core_flow: BleedFractionCoreFlow,
    *,
    xp: ArrayApiNamespace | None,
) -> t.ThrustN:
    """Absolute sea-level takeoff thrust with the Fig. 9 bleed fit."""
    return reference_thrust * takeoff_thrust_ratio_with_bleed(
        mach,
        bypass_ratio,
        gas_generator_function,
        hp_compressor_work_fraction,
        bleed_fraction_core_flow,
        xp=xp,
    )


def cruise_reference_specific_thrust(
    reference_thrust: t.ThrustN,
    reference_inlet_mass_flow: t.MassFlowKgPS,
) -> RefSpecificThrust:
    """Reference specific thrust $F^*/W_1^*$ in SI units."""
    return reference_thrust / reference_inlet_mass_flow


def cruise_inlet_mass_flow_from_fan_diameter(
    fan_diameter: t.LengthM,
) -> t.MassFlowKgPS:
    """Fig. 17 fit, expressed in SI."""
    fan_diameter_in = m_to_in(fan_diameter)
    inlet_mass_flow_lb_s = 0.0126192 * (fan_diameter_in - 14.11401) ** 2.56975
    return lb_to_kg(inlet_mass_flow_lb_s)


def cruise_tsfc_exponent_from_specific_thrust(
    reference_specific_thrust: RefSpecificThrust,
) -> ExponentN:
    """Fig. 16 fit for the Eq. (24) exponent `n`, expressed in SI."""
    specific_thrust_paper_units = nsperkg_to_lbfsperlb(
        reference_specific_thrust
    )
    return 6.13748 / (specific_thrust_paper_units + 3.4532) + 0.12695


def cruise_tsfc_exponent_from_thrust_and_mass_flow(
    reference_thrust: t.ThrustN,
    reference_inlet_mass_flow: t.MassFlowKgPS,
) -> ExponentN:
    """Convenience wrapper for the Fig. 16 exponent fit."""
    return cruise_tsfc_exponent_from_specific_thrust(
        cruise_reference_specific_thrust(
            reference_thrust,
            reference_inlet_mass_flow,
        )
    )


def cruise_tsfc_exponent_from_thrust_and_fan_diameter(
    reference_thrust: t.ThrustN,
    fan_diameter: t.LengthM,
) -> ExponentN:
    """Convenience wrapper Fig. 17 and Fig. 16 fits."""
    return cruise_tsfc_exponent_from_thrust_and_mass_flow(
        reference_thrust,
        cruise_inlet_mass_flow_from_fan_diameter(fan_diameter),
    )


def takeoff_linear_mach_coefficient(
    bypass_ratio: t.BypassRatio,
    gas_generator_function: GasGeneratorFunction,
) -> ExponentN:
    """Eq. (10)/(11) linear Mach coefficient."""
    return (
        0.377
        * (1 + bypass_ratio)
        / (((1 + 0.82 * bypass_ratio) * gas_generator_function) ** 0.5)
    )


def takeoff_quadratic_mach_coefficient(
    bypass_ratio: t.BypassRatio,
) -> ExponentN:
    """Eq. (10)/(11) quadratic Mach coefficient."""
    return 0.23 + 0.19 * bypass_ratio**0.5


def takeoff_altitude_intercept_factor(
    pressure_ratio: TakeoffAltitudePressureRatio,
) -> TakeoffAltitudeInterceptFactor:
    """Eq. (12), altitude-dependent intercept term `A`."""
    return -0.4327 * pressure_ratio**2 + 1.3855 * pressure_ratio + 0.0472


def takeoff_altitude_linear_factor(
    pressure_ratio: TakeoffAltitudePressureRatio,
) -> TakeoffAltitudeLinearMachFactor:
    """Eq. (13), altitude-dependent linear Mach scaling `Z`."""
    return (
        0.9106 * pressure_ratio**3
        - 1.7736 * pressure_ratio**2
        + 1.8697 * pressure_ratio
    )


def takeoff_altitude_quadratic_factor(
    pressure_ratio: TakeoffAltitudePressureRatio,
) -> TakeoffAltitudeQuadraticMachFactor:
    """Eq. (14), altitude-dependent quadratic Mach scaling `X`."""
    return (
        0.1377 * pressure_ratio**3
        - 0.4374 * pressure_ratio**2
        + 1.3003 * pressure_ratio
    )


def takeoff_thrust_ratio_polynomial(
    mach: t.MachNumber,
    bypass_ratio: t.BypassRatio,
    gas_generator_function: GasGeneratorFunction,
    intercept_factor: ExponentN = 1.0,
    linear_factor: TakeoffAltitudeLinearMachFactor = 1.0,
    quadratic_factor: TakeoffAltitudeQuadraticMachFactor = 1.0,
) -> ExponentN:
    """Core takeoff polynomial, Eqs. (8), (10), and (11)."""
    return (
        intercept_factor
        - linear_factor
        * takeoff_linear_mach_coefficient(bypass_ratio, gas_generator_function)
        * mach
        + quadratic_factor
        * takeoff_quadratic_mach_coefficient(bypass_ratio)
        * mach**2
    )


def takeoff_thrust_ratio_sea_level(
    mach: t.MachNumber,
    bypass_ratio: t.BypassRatio,
    gas_generator_function: GasGeneratorFunction,
) -> ExponentN:
    """Eq. (10), sea-level takeoff thrust ratio."""
    return takeoff_thrust_ratio_polynomial(
        mach,
        bypass_ratio,
        gas_generator_function,
    )


def takeoff_thrust_ratio(
    mach: t.MachNumber,
    pressure_ratio: TakeoffAltitudePressureRatio,
    bypass_ratio: t.BypassRatio,
    gas_generator_function: GasGeneratorFunction,
) -> ExponentN:
    """Eq. (11), altitude-adjusted takeoff thrust ratio without bleed.

    Customer bleed is intentionally excluded here. Bartel and Young provide a
    separate sea-level bleed fit (Fig. 9) but do not publish a combined
    altitude-plus-bleed model.
    """
    return takeoff_thrust_ratio_polynomial(
        mach,
        bypass_ratio,
        gas_generator_function,
        intercept_factor=takeoff_altitude_intercept_factor(pressure_ratio),
        linear_factor=takeoff_altitude_linear_factor(pressure_ratio),
        quadratic_factor=takeoff_altitude_quadratic_factor(pressure_ratio),
    )


def takeoff_thrust(
    reference_thrust: t.ThrustN,
    mach: t.MachNumber,
    pressure_ratio: TakeoffAltitudePressureRatio,
    bypass_ratio: t.BypassRatio,
    gas_generator_function: GasGeneratorFunction,
) -> t.ThrustN:
    """Absolute altitude-adjusted takeoff thrust from an SLS reference.

    The reference thrust is the sea-level static takeoff thrust $F_0$.
    """
    return reference_thrust * takeoff_thrust_ratio(
        mach,
        pressure_ratio,
        bypass_ratio,
        gas_generator_function,
    )


def climb_segment_3_speed_factor(
    mach: t.MachNumber,
    reference_mach: t.MachNumber,
) -> ExponentN:
    """Eq. (16), segment-3 speed correction `b`."""
    return (mach / reference_mach) ** -0.11


def climb_segment_3_parameter_d(
    mach_ratio: MachRatio, xp: ArrayApiNamespace | None
) -> ExponentN:
    """Table 2, linearly interpolated in `M/M_ref`."""
    return linear_interp(mach_ratio, TABLE_2_MACH_RATIOS, TABLE_2_D, xp=xp)


def climb_segment_3_thrust_ratio(
    ambient_to_reference_pressure_ratio: PressureRatioTo30kFt,
    parameter_d: ExponentN,
    speed_factor: ExponentN,
    *,
    xp: ArrayApiNamespace | None,
) -> ExponentN:
    """Eq. (15), climb segment 3 thrust ratio."""
    xpr = math if xp is None else xp
    return (
        parameter_d * xpr.log(ambient_to_reference_pressure_ratio)
        + speed_factor
    )


def climb_segment_3_thrust(
    reference_thrust: t.ThrustN,
    ambient_pressure: t.StaticPressurePA,
    reference_pressure: t.StaticPressurePA,
    mach: t.MachNumber,
    reference_mach: t.MachNumber,
    *,
    xp: ArrayApiNamespace | None,
) -> t.ThrustN:
    """Convenience wrapper for climb segment 3."""
    mach_ratio = mach / reference_mach
    return reference_thrust * climb_segment_3_thrust_ratio(
        ambient_pressure / reference_pressure,
        climb_segment_3_parameter_d(mach_ratio, xp=xp),
        climb_segment_3_speed_factor(mach, reference_mach),
        xp=xp,
    )


def climb_segment_2_speed_factor(
    calibrated_airspeed: t.CasMPS,
    reference_calibrated_airspeed: t.CasMPS,
) -> ExponentN:
    """Eq. (18), segment-2 speed correction `a`."""
    return (calibrated_airspeed / reference_calibrated_airspeed) ** -0.1


def climb_rate_exponent(
    climb_rate: ClimbRate,
) -> ExponentN[float]:
    """Table 3, climb-rate exponent `n`."""
    return TABLE_3_N[climb_rate]


def climb_segment_2_thrust_ratio(
    ambient_to_reference_pressure_ratio: PressureRatioTo30kFt,
    calibrated_airspeed: t.CasMPS,
    reference_calibrated_airspeed: t.CasMPS,
    exponent_n: ExponentN | ExponentN[float],
) -> ExponentN:
    """Eq. (17), climb segment 2 thrust ratio."""
    speed_ratio = calibrated_airspeed / reference_calibrated_airspeed
    exponent = -0.355 * speed_ratio + exponent_n
    return (
        climb_segment_2_speed_factor(
            calibrated_airspeed,
            reference_calibrated_airspeed,
        )
        * ambient_to_reference_pressure_ratio**exponent
    )


def climb_segment_2_thrust(
    reference_thrust: t.ThrustN,
    ambient_pressure: t.StaticPressurePA,
    reference_pressure: t.StaticPressurePA,
    calibrated_airspeed: t.CasMPS,
    reference_calibrated_airspeed: t.CasMPS,
    climb_rate: ClimbRate,
) -> t.ThrustN:
    """Convenience wrapper for climb segment 2."""
    return reference_thrust * climb_segment_2_thrust_ratio(
        ambient_pressure / reference_pressure,
        calibrated_airspeed,
        reference_calibrated_airspeed,
        climb_rate_exponent(climb_rate),
    )


def climb_segment_1_slope(
    cas_ratio: CasRatio,
    climb_rate: ClimbRate,
    *,
    xp: ArrayApiNamespace | None,
) -> ExponentN:
    """Table 4, linearly interpolated in `V_cas/V_casref`."""
    return linear_interp(
        cas_ratio, TABLE_4_CAS_RATIOS, TABLE_4_M[climb_rate], xp=xp
    )


def climb_segment_1_thrust_ratio(
    ambient_to_reference_pressure_ratio: PressureRatioTo30kFt,
    pressure_ratio_at_segment_boundary: PressureRatioTo30kFt,
    thrust_ratio_at_segment_boundary: ExponentN,
    slope: ExponentN,
) -> ExponentN:
    """Eq. (19), climb segment 1 thrust ratio.

    The segment boundary is the 10,000 ft transition point used by the paper.
    """
    return slope * ambient_to_reference_pressure_ratio + (
        thrust_ratio_at_segment_boundary
        - slope * pressure_ratio_at_segment_boundary
    )


def climb_segment_1_thrust(
    reference_thrust: t.ThrustN,
    ambient_pressure: t.StaticPressurePA,
    reference_pressure: t.StaticPressurePA,
    pressure_at_segment_boundary: t.StaticPressurePA,
    calibrated_airspeed: t.CasMPS,
    reference_calibrated_airspeed: t.CasMPS,
    climb_rate: ClimbRate,
    *,
    xp: ArrayApiNamespace | None,
) -> t.ThrustN:
    """Convenience wrapper for climb segment 1.

    The segment boundary is the 10,000 ft point at which Eq. (17) supplies the
    starting value `F_10/F_30` before Eq. (19) is applied.
    """
    speed_ratio = calibrated_airspeed / reference_calibrated_airspeed
    return reference_thrust * climb_segment_1_thrust_ratio(
        ambient_pressure / reference_pressure,
        pressure_at_segment_boundary / reference_pressure,
        climb_segment_2_thrust_ratio(
            pressure_at_segment_boundary / reference_pressure,
            calibrated_airspeed,
            reference_calibrated_airspeed,
            climb_rate_exponent(climb_rate),
        ),
        climb_segment_1_slope(speed_ratio, climb_rate, xp=xp),
    )


def cruise_tsfc_thrust_factor(
    mach: t.MachNumber,
    reference_mach: t.MachNumber,
    thrust: t.ThrustN,
    reference_thrust: t.ThrustN,
    *,
    xp: ArrayApiNamespace | None,
) -> ThrustFactorZ:
    """Eqs. (22) and (23).

    The paper uses the thrust correction when $M/M^* > 1$, while the
    factor itself is still expressed in terms of $F/F^*$.
    """
    mach_ratio = mach / reference_mach
    thrust_ratio = thrust / reference_thrust
    return where(mach_ratio > 1.0, thrust_ratio**-0.1, lambda: 1.0, xp=xp)


def cruise_tsfc_ratio(
    mach: t.MachNumber,
    reference_mach: t.MachNumber,
    exponent_n: ExponentN,
    thrust_factor: ThrustFactorZ,
) -> TsfcRatio:
    """Eq. (24), cruise TSFC ratio above 35,000 ft."""
    return thrust_factor * (mach / reference_mach) ** exponent_n


def cruise_tsfc(
    reference_tsfc: t.SpecificFuelConsumptionKgPNPS,
    mach: t.MachNumber,
    reference_mach: t.MachNumber,
    exponent_n: ExponentN,
    thrust: t.ThrustN,
    reference_thrust: t.ThrustN,
    *,
    xp: ArrayApiNamespace | None,
) -> t.SpecificFuelConsumptionKgPNPS:
    """Absolute cruise TSFC from Eq. (24)."""
    return reference_tsfc * cruise_tsfc_ratio(
        mach,
        reference_mach,
        exponent_n,
        cruise_tsfc_thrust_factor(
            mach,
            reference_mach,
            thrust,
            reference_thrust,
            xp=xp,
        ),
    )
