from typing import Annotated

from .quantity import GravitationalAcceleration

G_0: Annotated[float, GravitationalAcceleration("m s⁻²")] = 9.80665
"""Standard gravitational acceleration at sea level"""
