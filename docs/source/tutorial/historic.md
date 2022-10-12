# Converting historical data

Apart from manually adding new aircraft to the simulation environment, AirTrafficSim can also automatically convert historical data and generate and add aircraft into the simulation environment. The ConvertHistoricDemo class in `environment/ConvertHistoricDemo.py` provides a sample to set up such an environment.


## Detecting procedures and entry points

AirTrafficSim can detect the arrival and approach procedure of each flight base on historical data files. After detecting the procedures, AirTrafficSim will detect and store the entry position, time, and state e of each aircraft base on a user-defined rule such as distance to a location. 

```{code-block} python
---
lineno-start: 23
emphasize-lines: 33, 35, 39, 40, 41, 42, 43, 44
caption: ConvertHistoricDemo.py
---
# Location of the historic data
self.historic_data_path = Path(__file__).parent.parent.resolve().joinpath('data/flight_data/2018-05-01/')

print("Analyzing flight data")
# Set up arrival and approach data
arrivals_dict, arrival_waypoints_coord_dict = get_arrival_data("VHHH", "07R")
approach_dict, approach_waypoints_coord_dict = get_approach_data("VHHH", "07R")

# Storage for historic aircraft data
self.call_sign = []
self.type = []
self.star = []
self.approach = []
self.position = []
self.speed = []
self.start_alt = []
self.heading = []
self.time = []
self.aircraft_list = {}

# Loop all historic data files
for file in self.historic_data_path.iterdir():
        self.call_sign.append(file.name.removesuffix('.csv'))
        
        # Read and simplify flight trajectory
        df = pd.read_csv(file)
        traj = df[['lat', 'long']].to_numpy()
        simplified = np.array(rdp(traj, 0.005))   

        self.type.append(df['Aircraft_model'].iloc[0])

        # Detect arrival and approach procedures
        arrival_result, arrival_trajectory  = detect_sid_star(simplified, arrivals_dict, arrival_waypoints_coord_dict)
        self.star.append(arrival_result)
        approach_result, approach_trajectory = detect_sid_star(simplified, approach_dict, approach_waypoints_coord_dict)
        self.approach.append(approach_result)

        # Determine aircraft appearance point (150km to hong kong)
        index = np.where(Cal.cal_great_circle_dist(traj[:, 0], traj[:, 1], 22.3193, 114.1694) < 200)[0][0]
        self.position.append(traj[index])
        self.speed.append(df['gspeed'].iloc[index])
        self.start_alt.append(df['alt'].iloc[index])
        self.heading.append(df['hangle'].iloc[index])
        self.time.append(df['timestamp'].iloc[index])

        print(file.name.removesuffix('.csv'), arrival_result, approach_result)

print("Finished analyzing data")

# Get starting time
self.time = np.array(self.time)
```

## Adding and deleting aircraft

After converting historical flight data, AirTrafficSim will add aircraft at each timestep based on the stored entry time information. The aircraft will also be deleted if the aircraft has completed its flight plan and there is no next waypoint.

```{code-block} python
---
lineno-start: 85
caption: ConvertHistoricDemo.py
---
def atc_command(self):
    # Handle creation and deletion of aircraft
    time = self.start_time + timedelta(seconds=self.global_time)
    time = int(time.timestamp())
    index = np.where(self.time == time)[0]
    # Add aircraft
    for i in index:
        self.aircraft_list[self.call_sign[i]] = Aircraft(self.traffic, call_sign=self.call_sign[i], aircraft_type=self.type[i], flight_phase=FlightPhase.CRUISE, configuration=Config.CLEAN,
                                                            lat=self.position[i][0], long=self.position[i][1], alt=self.start_alt[i], heading=self.heading[i], cas=self.speed[i], fuel_weight=10000.0, payload_weight=12000.0,
                                                            arrival_airport="VHHH", arrival_runway="07R", star = self.star[i], approach = self.approach[i], cruise_alt=37000)
    # Delete aircraft
    index = self.traffic.index[self.traffic.ap.hv_next_wp == False]
    for i in index:
        self.traffic.del_aircraft(i)
```

## Holding and vectoring

A demo program is written to demonstrate the control of vectoring and holding.

```{code-block} python
---
lineno-start: 94
caption: ConvertHistoricDemo.py
---
# User algorithm
# Holding and vectoring
if "5J150" in self.aircraft_list:
    # self.aircraft_list["5J150"].set_vectoring(60, 195, "GUAVA")
    if self.global_time == 1600:
        self.aircraft_list["5J150"].set_holding(2, "BETTY", "VH")
```