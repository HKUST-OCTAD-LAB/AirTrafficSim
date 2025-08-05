from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import types as t

#
# ICAO International Standard Atmosphere.
#
# Assumptions:
#
# - air is dry, calorically perfect, perfect gas ($p = \rho R T$).
# - atmosphere is in hydrostatic equilibrium ($\frac{dp}{dz} = -\rho g$).
#
H_BELOW_TROP: t.GeopotentialAltitudeM[float] = 11000.0
"""
The tropopause is the separation between the troposphere and the stratosphere.
In ISA, its geopotential altitude is constant.
"""
BETA_BELOW_TROP: t.TemperatureGradientKPM[float] = -0.0065

T_0: t.StaticTemperatureK[float] = 288.15
P_0: t.StaticPressurePA[float] = 101325.0
RHO_0: t.DensityKGM3[float] = 1.225
A_0: t.SpeedOfSoundMPS[float] = 340.294


T_11: t.StaticTemperatureK[float] = 216.65
P_11: t.StaticPressurePA[float] = 22632.06
