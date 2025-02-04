"""
List of aircraft types, from [ICAO DOC8643](https://www.icao.int/publications/DOC8643/Pages/default.aspx)

Requires:

- airtrafficsim installed with extras `network`, `polars`
"""

from io import BytesIO

import httpx
import polars as pl

SCHEMA_AIRCRAFT_TYPES = {
    "ModelFullName": pl.String(),
    "Description": pl.String(),  # TODO: (enum with 39 values)
    "WTC": pl.Enum(["H", "M", "L", "J", "L/M"]),
    "WTG": pl.Enum(["E", "Z", "F", "C", "D", "G", "A", "B"]),
    "Designator": pl.String(),
    "ManufacturerCode": pl.String(),
    "ShowInPart3Only": pl.Boolean(),
    "AircraftDescription": pl.Enum(
        [
            "Helicopter",
            "SeaPlane",
            "LandPlane",
            "Tiltrotor",
            "Gyrocopter",
            "Amphibian",
        ]
    ),
    "EngineCount": pl.String(),  # for some reason there's a `C`
    "EngineType": pl.Enum(
        ["Piston", "Turboprop/Turboshaft", "Jet", "Rocket", "Electric"]
    ),
}
"""Schema for aircraft types dataset."""


SCHEMA_MANUFACTURERS = {
    "Code": pl.String(),
    "Names": pl.List(pl.String()),
    "StateName": pl.String(),
}
"""Schema for manufacturers dataset."""

#
# downloaders
#

URL_BASE_DOC8643 = "https://www4.icao.int/doc8643/External"


async def _post_and_parse_json(
    client: httpx.AsyncClient, url: str
) -> pl.DataFrame:
    response = await client.post(url)
    data = BytesIO(response.content)
    df = pl.read_json(data)
    return df


async def fetch_aircraft_types(client: httpx.AsyncClient) -> pl.DataFrame:
    df = await _post_and_parse_json(client, f"{URL_BASE_DOC8643}/AircraftTypes")
    return df.cast(SCHEMA_AIRCRAFT_TYPES)  # type: ignore


async def fetch_manufacturers(client: httpx.AsyncClient) -> pl.DataFrame:
    df = await _post_and_parse_json(client, f"{URL_BASE_DOC8643}/Manufacturers")
    return df.cast(SCHEMA_MANUFACTURERS)  # type: ignore
