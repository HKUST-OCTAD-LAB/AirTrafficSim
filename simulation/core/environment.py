import time
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import csv
from pathlib import Path

from utils.unit import Unit_conversion
from utils.enums import Flight_phase, Configuration, Speed_mode, Vertical_mode, AP_speed_mode, AP_throttle_mode, AP_vertical_mode, AP_lateral_mode
from core.traffic import Traffic


class Environment:
    """
    Base class for simulation environment
    """

    def __init__(self, file_name="default",  number_of_traffic=1000, start_time = datetime.utcnow(), end_time = 60, era5_weather=False, bada_perf=False):
        # User setting
        self.start_time = start_time
        """The simulation start time [datetime object]"""
        self.end_time = end_time
        """The simulation end time [s]"""

        # Simulation variable
        self.traffic = Traffic(number_of_traffic, file_name, start_time, end_time, era5_weather, bada_perf)
        self.global_time = 0                    # [s]

        # Handle io
        self.datetime = datetime.utcnow()
        self.last_sent_time = time.time()
        self.graph_type = 'None'
        self.packet_id = 0
        # Buffer
        self.time = []
        self.lat = []
        self.long = []
        self.alt = []
        self.cas = []

        # File IO
        self.file_name = file_name+'-'+self.datetime.isoformat(timespec='seconds')
        self.folder_path = Path(__file__).parent.parent.parent.resolve().joinpath('data/replay/simulation/'+self.file_name)
        self.folder_path.mkdir()
        self.file_path =  self.folder_path.joinpath(self.file_name+'.csv')
        self.writer = csv.writer(open(self.file_path, 'w+'))
        self.header = ['timestep','timestamp', 'id', 'callsign', 'lat', 'long', 'alt',
                        'cas', 'tas', 'mach', 'vs', 
                        'heading', 'bank_angle', 'path_angle',
                        'mass', 'fuel_consumed', 
                        'thrust', 'drag', 'esf', 'accel',
                        'ap_track_angle', 'ap_heading', 'ap_alt', 'ap_cas', 'ap_mach', 'ap_procedural_speed', 
                        'ap_wp_index', 'ap_next_wp', 'ap_dist_to_next_fix', 
                        'flight_phase', 'configuration', 'speed_mode', 'vertical_mode','ap_speed_mode', 'ap_lateral_mode']
        self.writer.writerow(self.header)
        self.header.remove('timestep')
        self.header.remove('timestamp')
        self.header.remove('id')
        self.header.remove('callsign')


    def atc_command(self):
        pass

    def should_end(self):
        """Return true/false of whether the simulation should end."""
        return False


    def run(self, socketio=None):
        if socketio:
            socketio.emit('simulationEnvironment', {'header': self.header, 'file': self.file_name})

        for i in range(self.end_time+1):
            # One timestep

            # Check if the simulation should end
            if self.should_end():
                self.end_time = self.global_time
                break

            start_time = time.time()

            # Run atc command
            self.atc_command()
            # Run update loop
            self.traffic.update(self.global_time)
            # Save to file
            self.save()

            print("Environment - step() for global time", self.global_time, "/", self.end_time, "finished at", time.time() - start_time, "seconds")
            
            if(socketio != None):
                # Save to buffer
                self.time.append((self.datetime + timedelta(seconds=self.global_time)).isoformat())
                self.lat.append(self.traffic.lat)
                self.long.append(self.traffic.long)
                self.alt.append(self.traffic.alt)
                self.cas.append(self.traffic.cas)

                @socketio.on('setSimulationGraphType')
                def set_simulation_graph_type(graph_type):
                    self.graph_type = graph_type

                now = time.time()
                if ((now - self.last_sent_time) > 0.5) or (self.global_time == self.end_time):
                    self.send_to_client(socketio)
                    socketio.sleep(0)
                    self.last_sent_time = now
                    self.time = []
                    self.lat = []
                    self.long = []
                    self.alt = []
                    self.cas = []

            self.global_time += 1
            
        print("")
        print("Export to CSVs")
        self.export_to_csv()
        print("")
        print("Simulation finished")


    def save(self):
        """
        Save all states variable of one timestemp to csv file.
        """
        data = np.column_stack((np.full(self.traffic.n, self.global_time), np.full(self.traffic.n, (self.datetime + timedelta(seconds=self.global_time)).isoformat(timespec='seconds')), np.arange(self.traffic.n), self.traffic.call_sign[:self.traffic.n], self.traffic.lat[:self.traffic.n], self.traffic.long[:self.traffic.n], self.traffic.alt[:self.traffic.n],
                                self.traffic.cas[:self.traffic.n], self.traffic.tas[:self.traffic.n], self.traffic.mach[:self.traffic.n], self.traffic.vs[:self.traffic.n], 
                                self.traffic.heading[:self.traffic.n], self.traffic.bank_angle[:self.traffic.n], self.traffic.path_angle[:self.traffic.n], 
                                self.traffic.mass[:self.traffic.n], self.traffic.fuel_consumed[:self.traffic.n],
                                self.traffic.perf.thrust[:self.traffic.n], self.traffic.perf.drag[:self.traffic.n], self.traffic.perf.esf[:self.traffic.n], self.traffic.accel[:self.traffic.n],
                                self.traffic.ap.track_angle[:self.traffic.n], self.traffic.ap.heading[:self.traffic.n], self.traffic.ap.alt[:self.traffic.n], self.traffic.ap.cas[:self.traffic.n], self.traffic.ap.mach[:self.traffic.n], self.traffic.ap.procedure_speed [:self.traffic.n],
                                self.traffic.ap.flight_plan_index[:self.traffic.n], [self.traffic.ap.flight_plan_name[i][val] if (val < len(self.traffic.ap.flight_plan_name[i])) else "NONE" for i, val in enumerate(self.traffic.ap.flight_plan_index[:self.traffic.n])], self.traffic.ap.dist[:self.traffic.n],                  # autopilot variable
                                [Flight_phase(i).name for i in self.traffic.flight_phase[:self.traffic.n]], [Configuration(i).name for i in self.traffic.configuration[:self.traffic.n]], [Speed_mode(i).name for i in self.traffic.speed_mode[:self.traffic.n]], [Vertical_mode(i).name for i in self.traffic.vertical_mode[:self.traffic.n]], 
                                [AP_speed_mode(i).name for i in self.traffic.ap.speed_mode[:self.traffic.n]], [AP_lateral_mode(i).name for i in self.traffic.ap.lateral_mode[:self.traffic.n]])) # mode
        
        self.writer.writerows(data)


    def export_to_csv(self):
        df = pd.read_csv(self.file_path)
        for id in df['id'].unique():
            df[df['id'] == id].to_csv(self.folder_path.joinpath(str(id)+'.csv'), index=False)
        # self.file_path.unlink()


    def send_to_client(self, socketio):
        print("send to client")

        document = [{
                "id": "document",
                "name": "simulation",
                "version": "1.0",
                "clock": {
                    "interval": self.datetime.isoformat()+"/"+(self.datetime + timedelta(seconds=self.end_time)).isoformat(),
                    "currentTime": self.datetime.isoformat(),
                }
            }]


        lat = np.vstack(tuple(self.lat))
        long = np.vstack(tuple(self.long))
        alt = np.vstack(tuple(self.alt))
        cas = np.vstack(tuple(self.cas))

        for i in range(self.traffic.n):
            positions = np.column_stack((np.array(self.time, dtype="object"), long[:,i], lat[:,i], Unit_conversion.feet_to_meter(alt[:,i]))).flatten().tolist()
            label = [{"interval": time+"/"+(self.datetime + timedelta(seconds=self.end_time)).isoformat(), 
                    "string": self.traffic.call_sign[i]+"\n"+str(np.floor(alt))+"ft "+str(np.floor(cas))+"kt"} 
                    for time, alt, cas in zip(self.time, alt[:,i], cas[:,i])]
            
            trajectory = {
                    "id": self.traffic.call_sign[i],
                    "position": {
                        "cartographicDegrees": positions
                    },
                    "point": {
                        "pixelSize": 5,
                        "color": {
                            "rgba": [39, 245, 106, 215]
                        }
                    },
                    "path": {
                        "leadTime": 0,
                        "trailTime": 20,
                        "distanceDisplayCondition": {
                            "distanceDisplayCondition": [0, 1500000]
                        }
                    },
                    "label": {
                        "text": label,
                        "font": "9px sans-serif",
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {
                            "cartesian2": [20, 20],
                        },
                        "distanceDisplayCondition": {
                            "distanceDisplayCondition": [0, 1500000]
                        },
                        "showBackground": "false",
                        "backgroundColor": {
                            "rgba": [0, 0, 0, 50]
                        }
                    }
                }
            document.append(trajectory)

        graph_data = []
        if self.graph_type != 'None':
            df = pd.read_csv(self.file_path)
            for id in df['id'].unique():
                content = df[df['id'] == id]
                graph_data.append({
                        "x": content['timestep'].to_list(),
                        "y": content[self.graph_type].to_list(),
                        "name": content.iloc[0]['callsign'],
                        "type": 'scattergl',
                        "mode": 'lines',
                    })  

        socketio.emit('simulationData', {'czml': document, 'progress': self.global_time/self.end_time, 'packet_id': self.packet_id,'graph': graph_data})
        self.packet_id = self.packet_id + 1
        
