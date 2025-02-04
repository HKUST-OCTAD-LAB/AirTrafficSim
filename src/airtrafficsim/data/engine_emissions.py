"""
[ICAO Aircraft Engine Emissions Databank](https://www.easa.europa.eu/en/domains/environment/icao-aircraft-engine-emissions-databank)

Requires:

- airtrafficsim installed with extras `network`, `polars`
"""

from io import BytesIO
from typing import NamedTuple

import httpx
import polars as pl

URL_EMISSIONS = "https://www.easa.europa.eu/en/downloads/131424/en"


async def _fetch_data(client: httpx.AsyncClient) -> bytes:
    response = await client.get(URL_EMISSIONS)
    return response.content


class EmissionsData(NamedTuple):
    data: pl.DataFrame
    schema: pl.DataFrame


def _parse_data(response_content: bytes) -> EmissionsData:
    data = BytesIO(response_content)
    df_schema = pl.read_excel(
        data, sheet_name="Column Description", read_options={"header_row": 18}
    ).rename(
        {
            "Column": "column",
            "Heading": "heading",
            "Description   (if different from Heading)": "description",
        }
    )
    df = pl.read_excel(data, sheet_name="Gaseous Emissions and Smoke")
    return EmissionsData(data=df, schema=df_schema)


async def fetch_emissions_data(client: httpx.AsyncClient) -> EmissionsData:
    response_content = await _fetch_data(client)
    return _parse_data(response_content)
