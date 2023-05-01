# Adding flight plan

AirTrafficSim can simulate flights following a user-defined flight plan. The `FullFlightDemo` class in `airtrafficsim_data/environment/FullFlightDemo.py` demonstrates how to set up a flight plan in AirTrafficSim. This tutorial simulates setting up a flight departing from the Hong Kong International Airport (VHHH) to the Taoyuan International Airport (RCTP) with SID and STAR.

 ## Parameters

In the add aircraft section of the init function of the `FullFlightDemo` class, the aircraft with callsign (FULL) is created. For the details of each parameter, you may reference [this section](./creating_env.md/#add-aircraft).

```{tip} 
You can get the runway coordinate through the function `Nav.get_runway_coord()`. In this sample, it is used to set up the initial condition `lat, long, alt`. 
```

In addition, some optional parameters are passed in this tutorial to create the aircraft including, `departure_airport`, `departure_runway`, `sid`, `arrival_airport`, `arrival_runway`, `star`, `approach`, `flight_plan`, and `cruise_alt`. These parameters are used for AirTrafficSim to generate a flight plan. 
 
```{code-block} python
---
lineno-start: 20
emphasize-lines: 2, 6, 7, 8, 9
caption: airtrafficsim_data/environment/FullFlightDemo.py
---
# Add aircraft
lat_dep, long_dep, alt_dep = Nav.get_runway_coord("VHHH", "25L")
self.aircraft_full = Aircraft(self.traffic, call_sign="FULL", aircraft_type="A320", flight_phase=FlightPhase.TAKEOFF, configuration=Config.TAKEOFF,
                                lat=lat_dep, long=long_dep, alt=alt_dep, heading=254.0, cas=149.0,
                                fuel_weight=5273.0, payload_weight=12000.0,
                                departure_airport = "VHHH", departure_runway="RW25L", sid = "OCEA2B",
                                arrival_airport="RCTP", arrival_runway="05R", star = "TONG1A", approach = "I05R",
                                flight_plan=["RASSE", "CONGA", "ENVAR", "DADON", "EXTRA", "RENOT"],
                                cruise_alt=37000)
```
 
 ## Departure/Arrival

 The waypoints and related restrictions of a Standard Terminal Arrival Procedure (STAR) and/or Standard Instrument Departure Route (SID) will be generated when the user provides information including airport, runway, and the procedure's ICAO code. 
 
 ## En-route

 `Flight_plan` and `cruise_alt` are used to generate the related plan for en-route navigation. `flight_plan` is a list of en-route waypoints in ICAO code where `cruise_alt` is the target cruise altitude in feet.

 ```{note}
Currently, airway and flight plan in ICAO format is not supported. We are working towards such functionality.
```