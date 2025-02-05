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

from __future__ import annotations

from typing import TYPE_CHECKING

from .geospatial import G_0

if TYPE_CHECKING:
    from dataclasses import dataclass
    from typing import Annotated

    from . import units as u

    @dataclass(frozen=True, slots=True)
    class Div:
        """
        A ratio between two untis

        Used in [unit conversion][airtrafficsim.unit_conversion].
        """

        numerator: u.UnitBase
        denominator: u.UnitBase

#
# base
#

HR_TO_MIN: Annotated[float, Div(u.MINUTE, u.HOUR)] = 60.0
MIN_TO_S: Annotated[float, Div(u.SECOND, u.MINUTE)] = 60.0
KILO = 1000
FT_TO_M: Annotated[float, Div(u.METER, u.FOOT)] = 0.3048
NMI_TO_M: Annotated[float, Div(u.METER, u.NMI)] = 1852.0
MI_TO_M: Annotated[float, Div(u.METER, u.MILE)] = 1609.344
LBM_TO_KG: Annotated[float, Div(u.KILOGRAM, u.POUND)] = 0.45359237
#
# derived
#

KT_TO_KPH: Annotated[float, Div(u.KPH, u.KT)] = NMI_TO_M / KILO  # 1.852
MPS_TO_KPH: Annotated[float, Div(u.KPH, u.MPS)] = (
    HR_TO_MIN * MIN_TO_S / KILO
)  # 3.6
MPH_TO_KPH: Annotated[float, Div(u.KPH, u.MPH)] = MI_TO_M / KILO  # 1.609344
KT_TO_MPS: Annotated[float, Div(u.MPS, u.KT)] = KT_TO_KPH / MPS_TO_KPH
FPM_TO_MPS: Annotated[float, Div(u.MPS, u.FPM)] = FT_TO_M / MIN_TO_S  # 0.00508
LBF_TO_N: Annotated[float, Div(u.NEWTON, u.POUND_FORCE)] = (
    LBM_TO_KG * G_0
)  # 4.4482216152605


LBLBFH_TO_KGNS: Annotated[float, Div(u.KGNS, u.LBLBFH)] = (
    LBM_TO_KG * (1 / LBF_TO_N) * (1 / 3600)
)
