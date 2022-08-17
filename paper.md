---
title: 'AirTrafficSim: An open-source web-based air traffic simulation platform.'
tags:
  - Python
  - air traffic management
authors:
  - name: Ka Yiu HUI
    # orcid: 0000-0000-0000-0000
    affiliation: 1
  - name: Chris HC. NGUYEN
    affiliation: 1
  - name: Go Nam LUI
    affiliation: 1
  - name: Rhea P. LIEM
    corresponding: true # (This is how to denote the corresponding author)
    affiliation: 1
affiliations:
 - name: Department of Mechanical and Aerospace Engineering, The Hong Kong University of Science and Technology, Hong Kong
   index: 1
date: 05 September 2022
bibliography: paper.bib
---

# Statement of need

Air traffic management (ATM) research traditionally focus on the macroscopic aspect of air transpotation such as airspace design research, traffic flow management, airport planning and scheduling, and more. Recently, as new aerial vehicles concepts, including Urban Air Mobility (UAM) and unmanned aircraft system (UAS) or drones, are being developed as well as raising consideration for sustainability, there has been a growing interst in performing microscopic ATM research such as conflict resolution using reinforcement learning, 4D-trajectory optimization, and even unmanned traffic management (UTM) development. Project U-space form Eurocontrol, FAA and NASA's UTM research project, airbus UTM are some of the examples that the industry and research community are focusing more on such reseach. 

However, most of the ATM simulation tools are commercial product aimed for the training of Air Traffic Controllers. ATM simulation tools for research purpose that are easily accessbile and open-source are still scarce. Bluesky [@BlueSky] is one of the few open-source packages for conducting ATM research. Therefore, AirTrafficSim was developed to facilitate ATM research. 

# Summary

AirTrafficSim is a web-based air traffic simulation software written in python and javascript. It is designed to visualize ATM research results, to provide a comprehensive software environment to perform microscopic study of air traffic movement such as reinforcement learning research, and to evaluate the performance of ATM algorithms. \autoref{fig:Architecture} shows the architecture of AirTrafficSim.

![Architecture of AirTrafficSim.\label{fig:Architecture}](figures/Architecture.png){ width=50% }

`AirTrafficSim` contains a user interface (UI) frontend written in javascript with Ionic React framework to provide an easy-to-use 3D UI to visualize both historic and simulated air traffic in a browser. The base 3D globes are powered with CesiumJS library to stream high-resolution maps, terrain, 3D building data, and to visualize dynamic geospatial data from simulation. The UI can also visualize the navigation and weather data which will be explained below. It can also plot the aircraft parameters in a simulation using the plotly library.

On the other hand, the backend of AirTrafficSim consists of several modules including navigation, weather, autopilot, performance, and flight route detection as shown in \autoref{fig:UI}. 

The **navigation** module provide global airports, Fixes, Navaids, Airways, Standard Instrument Departures (SIDs), Standard Terminal Arrival Routes (STARs), and Approaches procedure information using the navigation database from x-plane 11. 

The **weather** module provide historic weather information including multi-level wind, pressure, temperature, and single-level surface precipitation data from ECMWF ERA5 weather database. It also process radar images provided by user as a source of high-resolution abnormal weather information.

The **autopilot** module processes the flight plan and control the aircraft to follow the plan from take-off to landing in a full flight simulation. It can also control the aircraft based on the inputted target state (ATC command) by user and ATM algorithm. Non-standard manuevers that are sometimes used by Air Traffic Controllers such as vectoring, holding, and direct can also be commanded.

The **performance** module calculate the aircraft state, such as speed, heading, vertical rate, fuel consompution, per each timestep. Currently, `AirtrafficSim` makes use of the licensed BADA performance model data from EuroControl but it is extensible to other performance model such as the open-source openAP model.

The **flight route detection** module detects the flight route including origin and destination airports, SIDs, and STARs from historic flight data and generate a flight plan for simulation. A more robust algorithm are being developed to detect the airways in order to generate a complete flight plan.

![UI of AirTrafficSim showcasing different features. (Upper left: Fuel consumption of simulated flight. Upper right: Navigation waypoints. Lower left: ECMWF ERA5 Wind data. Lower right: HKO 256km radar image.)\label{fig:UI}](figures/UI.png){ width=100% }

# Acknowledgements

This project was supported by the Hong Kong Innovation and Technology Commission (Project No. ITS/016/20).

# References