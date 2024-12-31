import jax
import jax.numpy as jnp

from airtrafficsim.experimental.common import G_0
from airtrafficsim.experimental.performance.bada3 import atmosphere
from airtrafficsim.experimental.thermodynamics import R_SPECIFIC_DRY_AIR


def test_jax() -> None:
    """
    Test that the BADA3 atmosphere model can be differentiated with JAX,
    and that it is under hydrostatic equilibrium.
    """
    zs = jnp.linspace(0, 20000, 100)

    dpdz = jax.vmap(
        jax.grad(lambda z: atmosphere(z, delta_temperature=0.0).pressure)
    )(zs)
    rho = atmosphere(zs, delta_temperature=0.0).density(R_SPECIFIC_DRY_AIR)

    assert jnp.allclose(dpdz, -rho * G_0)
