"""
Useful constants

To convert between units, multiply by the appropriate constant.

# Examples

```pycon
>>> import numpy as np
>>> from airtrafficsim.unit_conversion import FEET_TO_METER
>>> h_meters = np.array([0., 11000., 20000.])
>>> h_ft = h_meters / FEET_TO_METER
>>> h_ft
array([    0.        , 36089.23884514, 65616.79790026])
>>> h_ft * FEET_TO_METER
array([    0., 11000., 20000.])
```

Unless or specified otherwise, numerical values are defined as exact by SI
"""

from typing import Annotated

from .annotations import (
    Force,
    Length,
    Mass,
    ThrustSpecificFuelConsumption,
    Time,
    Velocity,
)
from .geospatial import G_0

#
# base
#

HR_TO_MIN: Annotated[float, Time("min") / Time("h")] = 60.0
MIN_TO_S: Annotated[float, Time("s") / Time("min")] = 60.0
KILO = 1000
FT_TO_M: Annotated[float, Length("m") / Length("ft")] = 0.3048
NMI_TO_M: Annotated[float, Length("m") / Length("nmi")] = 1852.0
MI_TO_M: Annotated[float, Length("m") / Length("mi")] = 1609.344
LBM_TO_KG: Annotated[float, Mass("kg") / Mass("lbm")] = 0.45359237

#
# derived
#

KT_TO_KPH: Annotated[float, Velocity("km h⁻¹") / Velocity("kt")] = (
    NMI_TO_M / KILO
)  # 1.852
MPS_TO_KPH: Annotated[float, Velocity("km h⁻¹") / Velocity("m s⁻¹")] = (
    HR_TO_MIN * MIN_TO_S / KILO
)  # 3.6
MPH_TO_KPH: Annotated[float, Velocity("km h⁻¹") / Velocity("mi h⁻¹")] = (
    MI_TO_M / KILO
)  # 1.609344
KT_TO_MPS: Annotated[float, Velocity("m s⁻¹") / Velocity("kt")] = (
    KT_TO_KPH / MPS_TO_KPH
)
FPM_TO_MPS: Annotated[float, Velocity("m s⁻¹") / Velocity("ft min⁻¹")] = (
    FT_TO_M / MIN_TO_S
)  # 0.00508
LBF_TO_N: Annotated[float, Force("N") / Force("lbf")] = (
    LBM_TO_KG * G_0
)  # 4.4482216152605

LBLBFH_TO_KGNS: Annotated[
    float,
    ThrustSpecificFuelConsumption("kg s⁻¹ N⁻¹")
    / ThrustSpecificFuelConsumption("lb lbf h⁻¹"),
] = LBM_TO_KG * (1 / LBF_TO_N) * (1 / 3600)
