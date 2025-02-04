from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from airtrafficsim.data.aircraft_types import (
    fetch_aircraft_types,
    fetch_manufacturers,
)
from airtrafficsim.data.airports import fetch_airports
from airtrafficsim.data.engine_emissions import (
    fetch_emissions_data,
)


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(http2=True) as client:
        yield client


@pytest.mark.anyio
async def test_airports(async_client: AsyncClient) -> None:
    airports = await fetch_airports(async_client)
    assert len(airports) > 60_000


@pytest.mark.anyio
async def test_emissions_data(async_client: AsyncClient) -> None:
    emissions_data = await fetch_emissions_data(async_client)
    assert len(emissions_data.data) > 800


@pytest.mark.anyio
async def test_aircraft_types(async_client: AsyncClient) -> None:
    aircraft_types = await fetch_aircraft_types(async_client)
    assert len(aircraft_types) > 7_000


@pytest.mark.anyio
async def test_manufacturers(async_client: AsyncClient) -> None:
    manufacturers = await fetch_manufacturers(async_client)
    assert len(manufacturers) > 2_000


# TODO: add era5
