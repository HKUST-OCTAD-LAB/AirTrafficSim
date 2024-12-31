import numpy as np


def test_jax() -> None:
    """
    Test the differentiability of the BADA3 atmosphere model and that it is
    under hydrostatic equilibrium.
    """
    import jax
    import jax.numpy as jnp

    from airtrafficsim.experimental.geospatial import G_0
    from airtrafficsim.experimental.performance.bada3 import atmosphere
    from airtrafficsim.experimental.thermodynamics import R_SPECIFIC_DRY_AIR

    zs = jnp.linspace(0, 20000, 50)

    dpdz = jax.vmap(
        jax.grad(lambda z: atmosphere(z, delta_temperature=0.0).pressure)
    )(zs)
    rho = atmosphere(zs, delta_temperature=0.0).density(R_SPECIFIC_DRY_AIR)

    assert jnp.allclose(dpdz, -rho * G_0)


def test_eas_tas() -> None:
    from airtrafficsim.experimental.performance.airspeed import (
        eas_from_tas,
        tas_from_eas,
    )

    tas = np.linspace(10, 600, 50).reshape(1, -1)
    rho = np.linspace(1.225, 0.08803, 50).reshape(-1, 1)

    eas = eas_from_tas(tas, rho)
    tas2 = tas_from_eas(eas, rho)

    assert np.allclose(tas, tas2)


def test_cas_tas() -> None:
    from airtrafficsim.experimental.performance.airspeed import (
        cas_from_tas,
        tas_from_cas,
    )

    tas = np.linspace(10, 600, 50).reshape(1, 1, -1)
    rho = np.linspace(1.225, 0.08803, 50).reshape(1, -1, 1)
    p = np.linspace(101325, 5475, 50).reshape(-1, 1, 1)

    cas = cas_from_tas(tas, rho, p)
    tas2 = tas_from_cas(cas, rho, p)

    assert np.allclose(tas, tas2)
