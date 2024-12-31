!!! warning
    This module is considered deprecated and will not receive any maintenance.
    Please use the [experimental module][airtrafficsim.experimental] instead.

AirTrafficSim contains three main modules:

- `core`: Main simulation engine
- `server`: Networking and communication
- `utils`: Support utilities

## Core Module

The core modules handle all simulation task. The entry is the environment class while traffic class stores main traffic data array and hold other classes including navigation, autopilot, weather, and performance. The aircraft class provides you an interface to interact with each aircraft in traffic data array.

::: airtrafficsim.core.environment
::: airtrafficsim.core.aircraft
::: airtrafficsim.core.traffic
::: airtrafficsim.core.navigation
    options:
      members:
        - fix
        - nav
        - airports
        - airway
        - holding
        - min_off_route_alt
        - min_sector_alt
::: airtrafficsim.core.autopilot
::: airtrafficsim.core.performance.performance
::: airtrafficsim.core.performance.bada
::: airtrafficsim.core.weather.weather
::: airtrafficsim.core.weather.era5

## Server Module

The server modules handles the backend server and communication of AirTrafficSim. The entry point is server.py while replay.py and data.py provides support functions to handle data generation.

::: airtrafficsim.server.server
::: airtrafficsim.server.replay
::: airtrafficsim.server.data

## Utils Module

The utils module provides support functionality for the simulation.

::: airtrafficsim.utils.enums
::: airtrafficsim.utils.calculation
::: airtrafficsim.utils.unit_conversion

## Misc

::: airtrafficsim.geometry
::: airtrafficsim.types