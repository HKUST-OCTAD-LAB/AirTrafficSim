"""
List of airports, from [ourairports](https://ourairports.com/data/)

Requires:

- airtrafficsim installed with extras `network`, `polars`
"""

from io import BytesIO
from pathlib import Path

import httpx
import polars as pl

#
# wrappers
#

SCHEMA_AIRPORTS = {
    "id": pl.Int32(),
    "ident": pl.String(),
    "type": pl.String(),
    "name": pl.String(),
    "latitude_deg": pl.Float32(),
    "longitude_deg": pl.Float32(),
    "elevation_ft": pl.Int16(),
    "continent": pl.String(),
    "iso_country": pl.String(),
    "iso_region": pl.String(),
    "municipality": pl.String(),
    "scheduled_service": pl.String(),
    "gps_code": pl.String(),
    "iata_code": pl.String(),
    "local_code": pl.String(),
    "home_link": pl.String(),
    "wikipedia_link": pl.String(),
    "keywords": pl.String(),
}
"""Schema for airports dataset."""


def scan_airports(fp: Path) -> pl.LazyFrame:
    """
    Lazily load list of airports from parquet file.

    Schema: [airtrafficsim.data.airports.SCHEMA_AIRPORTS][]
    """
    if not fp.exists():
        raise FileNotFoundError(
            "cannot find airports\nhelp: download it first."
        )
    return pl.scan_parquet(fp, schema=SCHEMA_AIRPORTS)


#
# downloaders
#

URL_BASE = "https://davidmegginson.github.io/ourairports-data"


async def fetch_airports(client: httpx.AsyncClient) -> pl.DataFrame:
    """
    Download all airports from ourairports.

    Schema: [airtrafficsim.data.airports.SCHEMA_AIRPORTS][]
    """
    response = await client.get(f"{URL_BASE}/airports.csv")
    data = BytesIO(response.content)

    airports = pl.read_csv(data, schema=SCHEMA_AIRPORTS).cast(SCHEMA_AIRPORTS)  # type: ignore
    return airports
