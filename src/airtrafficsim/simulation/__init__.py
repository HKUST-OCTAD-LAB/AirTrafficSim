"""
An experimental simulation engine, inspired by archetype-based
entity-component-systems (ECS).

Unlike traditional OOP engines with deep inheritance, it has:

- **Entities** that do not own any data, but an *index*
- **Components** are `Vec<T>`s holding plain old data
- **Systems** that query / operate on a combination of components

**Archetypes** are a unique set of components, represented as tables,
where columns are components and rows are entities.

This could be thought of an SQL database.

# Example

```txt
Table `airports`:
   lng  lat  icao  ...
1   .    .    .        <- entity
2   .    .    .
3   .    .    .
    ^
component

Table `aircraft` components: `lng`, `lat`, `callsign`, `ground_speed` ...
Table `waypoints` components: `lng`, `lat`, `name`, `type`, ...
```

A system might:

- perform forward Euler on all aircraft positions
- query the closest airport for each aircraft

# Advantages

- columnar layout enables:
    - high performance with array operations
    - easy serialisation to parquet files
- data oriented design
- loose coupling

# Disadvantages

- poor insertion and deletion performance

See:

- https://docs.rs/hecs/
- https://www.flecs.dev/
- https://docs.unity3d.com/Packages/com.unity.entities@0.17/manual/ecs_core.html
"""

from dataclasses import dataclass, field
from typing import NewType

import polars as pl

TableName = NewType("TableName", str)


@dataclass
class Table:
    name: TableName
    df: pl.DataFrame


@dataclass
class World:
    tables: dict[TableName, Table] = field(default_factory=dict)
