from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np

from airtrafficsim.core.environment import Environment
from airtrafficsim.core.aircraft import Aircraft
from airtrafficsim.utils.enums import Config, FlightPhase
from airtrafficsim.utils.calculation import Cal
from airtrafficsim.utils.route_detection import rdp, detect_sid_star, get_arrival_data, get_approach_data

class ConvertHistoricDemo(Environment):

    def __init__(self):
        # Initialize environment super class
        super().__init__(file_name = Path(__file__).name.removesuffix('.py'), #File name (do not change)
                        start_time = datetime.fromisoformat('2018-05-01T00:00:00+00:00'),
                        end_time = 3600*2,
                        weather_mode = "",
                        performance_mode = "BADA" 
                        )

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


    def should_end(self):
        return False

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

        # User algorithm
        # Holding and vectoring
        if "5J150" in self.aircraft_list:
            # self.aircraft_list["5J150"].set_vectoring(60, 195, "GUAVA")
            if self.global_time == 1600:
                self.aircraft_list["5J150"].set_holding(2, "BETTY", "VH")
        

        