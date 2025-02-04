import numpy as np

ATMOSPHERE_TEST = {
    "z": np.linspace(0, 20000, 50),
    "tas": np.linspace(10, 600, 50),
    "rho": np.linspace(1.225, 0.08803, 50),
    "p": np.linspace(101325, 5475, 50),
}  # NOTE: fake data, not ISA!


def test_jax() -> None:
    """
    Test the differentiability of the BADA3 atmosphere model and that it is
    under hydrostatic equilibrium.
    """
    import jax
    import jax.numpy as jnp

    from airtrafficsim.geospatial import G_0
    from airtrafficsim.performance.bada3 import atmosphere
    from airtrafficsim.thermodynamics import R_SPECIFIC_DRY_AIR

    zs = ATMOSPHERE_TEST["z"]

    dpdz = jax.vmap(
        jax.grad(lambda z: atmosphere(z, delta_temperature=0.0).pressure)
    )(zs)
    rho = atmosphere(zs, delta_temperature=0.0).density(R_SPECIFIC_DRY_AIR)

    assert jnp.allclose(dpdz, -rho * G_0)


def test_polars_extension() -> None:
    """Check support for polars lazy API"""
    import polars as pl

    from airtrafficsim.performance.bada3 import atmosphere

    def pressure(expr: pl.Expr) -> tuple[pl.Expr, pl.Expr]:
        res = atmosphere(expr, delta_temperature=0.0)
        return (
            res.pressure.alias("pressure"),
            res.temperature.alias("temperature"),
        )

    df = pl.DataFrame(ATMOSPHERE_TEST).lazy()
    values = df.select(pressure(pl.col("z"))).collect()

    expected = atmosphere(np.array(ATMOSPHERE_TEST["z"]), delta_temperature=0.0)
    assert np.allclose(values["pressure"], expected.pressure)
    assert np.allclose(values["temperature"], expected.temperature)


def test_eas_tas() -> None:
    from airtrafficsim.performance.airspeed import (
        eas_from_tas,
        tas_from_eas,
    )

    tas = ATMOSPHERE_TEST["tas"].reshape(1, -1)
    rho = ATMOSPHERE_TEST["rho"].reshape(-1, 1)

    eas = eas_from_tas(tas, rho)
    tas2 = tas_from_eas(eas, rho)

    assert np.allclose(tas, tas2)


def test_cas_tas() -> None:
    from airtrafficsim.performance.airspeed import (
        cas_from_tas,
        tas_from_cas,
    )

    tas = ATMOSPHERE_TEST["tas"].reshape(1, 1, -1)
    rho = ATMOSPHERE_TEST["rho"].reshape(1, -1, 1)
    p = ATMOSPHERE_TEST["p"].reshape(-1, 1, 1)

    cas = cas_from_tas(tas, rho, p)
    tas2 = tas_from_cas(cas, rho, p)

    assert np.allclose(tas, tas2)
