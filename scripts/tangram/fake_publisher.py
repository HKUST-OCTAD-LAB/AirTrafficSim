#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "redis",
# ]
# ///
from __future__ import annotations

import asyncio
import json
import logging
import math
import os
import random
import time
from typing import TypeAlias, TypedDict

from redis.asyncio import Redis

REDIS_CHANNEL: str = os.getenv("REDIS_CHANNEL", "jet1090")
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
NUM_AIRCRAFT = 100
DEGREES_PER_SEC = 0.1
UPDATE_INTERVAL_SEC = 0.5


class StateVector(TypedDict):
    lat: float
    lon: float
    alt: float
    track: float
    callsign: str


def create_initial_state(i: int) -> StateVector:
    return {
        "lat": random.uniform(-70.0, 70.0),
        "lon": random.uniform(-180.0, 180.0),
        "alt": random.uniform(10000, 42000),
        "track": random.uniform(0, 360),
        "callsign": f"FAKE{i:04d}",
    }


Icao: TypeAlias = str

AIRCRAFT: dict[Icao, StateVector] = {
    f"{random.randint(0, 0xFFFFFF):06x}": create_initial_state(i)
    for i in range(NUM_AIRCRAFT)
}


def update_position(aircraft_state: StateVector) -> None:
    lat, lon, track = (
        aircraft_state["lat"],
        aircraft_state["lon"],
        aircraft_state["track"],
    )

    track_rad = math.radians(track)
    lat_rad = math.radians(lat)

    delta_lat = DEGREES_PER_SEC * math.cos(track_rad)
    delta_lon = DEGREES_PER_SEC * math.sin(track_rad) / math.cos(lat_rad)

    new_lat = lat + delta_lat
    new_lon = lon + delta_lon

    aircraft_state["lat"] = max(-90.0, min(90.0, new_lat))
    dlon = -360 if new_lon > 180 else 360 if new_lon < -180 else 0
    aircraft_state["lon"] = new_lon + dlon


async def main() -> None:
    redis_client = await Redis.from_url(REDIS_URL)
    await redis_client.ping()
    logging.info(f"connected to redis at {REDIS_URL}")
    logging.info(
        f"publishing to channel '{REDIS_CHANNEL}' for {NUM_AIRCRAFT} aircraft"
    )

    while True:
        for icao, state in AIRCRAFT.items():
            update_position(state)

            payload = {
                "icao24": icao,
                "df": "17",  # downlink format 17 (ADS-B)
                "bds": "09",  # contains airborne velocity
                "timestamp": time.time(),
                "callsign": state["callsign"],
                "altitude": state["alt"],
                "latitude": state["lat"],
                "longitude": state["lon"],
                "track": state["track"],
                "groundspeed": 450 + random.randint(-10, 10),
            }

            await redis_client.publish(REDIS_CHANNEL, json.dumps(payload))

        logging.debug("published updates")
        await asyncio.sleep(UPDATE_INTERVAL_SEC)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.DEBUG)
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)
