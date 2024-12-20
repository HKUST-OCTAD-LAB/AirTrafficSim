from typing import TypeVar

import numpy as np
import numpy.typing as npt

array = npt.NDArray[np.floating]
"""A numpy array of floating point numbers."""
# NOTE: not using npt.ArrayLike because it accepts strings

ArrayOrFloat = TypeVar("ArrayOrFloat", array, float)

uint_array = npt.NDArray[np.unsignedinteger]
"""A numpy array of unsigned integers."""
# for use in array of enums
