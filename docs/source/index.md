# AirTrafficSim

AirTrafficSim is a web-based air traffic simulation software written in Python and Javascript. It is designed to visualize historical and research data, perform microscopic studies of air traffic movement with the integration of a historical weather database, and evaluate the performance of ATM algorithms.

AirTrafficSim is open-sourced at [https://github.com/HKUST-OCTAD-LAB/AirTrafficSim](https://github.com/HKUST-OCTAD-LAB/AirTrafficSim).

## Features

- Replay historical flights given data (FlightRadar 24 and simulated flights)
- Air traffic simulation using [BADA performance data](https://www.eurocontrol.int/model/bada) and OpenAP (WIP)
- Navigation data simulation and visualization from [x-plane 11](https://developer.x-plane.com/docs/data-development-documentation/)
- Autopilot and Flight Management System simulation
- Holding, vectoring, direct to maneuvers simulation
- Weather data from [ECMWF ERA5](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=overview) and custom radar image
- Air traffic is controlled with Python API interface to simulate ATC interaction

```{image} images/UI_features.png
```

## Usages

> **Tactical routing for air transportation in HKIA terminal manuevering area.**
> 
> The 26th HKSTS International Conference, 2022
> 
> Chris HC. NGUYEN, Go Nam LUI, Ka Yiu HUI, and Rhea P. LIEM

<div>
<iframe width="560" height="315" src="https://www.youtube.com/embed/Vq62IG-sNQY" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>


```{toctree}
   :hidden:
   
   Installation <install>
   Getting started <start>
```

```{toctree}
   :caption: Tutorial
   :hidden:
   
   Navigating the UI <tutorial/UI>
   Understanding the project structure <tutorial/structure>
   Replaying data <tutorial/replay>
   Creating a simulation environment <tutorial/creating_env>
   Running a simulation <tutorial/simulation>
   Adding flight plan <tutorial/flight_plan>
   Using historical weather database <tutorial/weather>
   Converting historical data <tutorial/historic>
```

```{toctree}
   :caption: Development
   :hidden:
   
   Development guide <development/guide>
   Client <development/client>
   Documentation <development/documentation>
   API reference <api/index>
```