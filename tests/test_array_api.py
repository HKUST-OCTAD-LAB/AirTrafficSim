import pytest

import numpy as np
from airtrafficsim.array_api import linear_interp


@pytest.mark.parametrize(
    ("x", "left", "right"),
    [
        (-1.0, None, None),
        (0.0, None, None),
        (0.5, None, None),
        (1.5, None, None),
        (3.0, None, None),
        (-1.0, -5.0, 99.0),
        (3.0, -5.0, 99.0),
    ],
)
def test_linear_interp_python_matches_numpy(
    x: float,
    left: float | None,
    right: float | None,
) -> None:
    xs = (0.0, 1.0, 2.0)
    fs = (10.0, 20.0, 50.0)

    expected = float(np.interp(x, xs, fs, left=left, right=right))
    actual = linear_interp(x, xs, fs, left=left, right=right, xp=None)

    assert actual == pytest.approx(expected)
