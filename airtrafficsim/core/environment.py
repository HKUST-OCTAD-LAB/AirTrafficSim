import time
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import csv
from pathlib import Path

from airtrafficsim.utils.unit_conversion import Unit
from airtrafficsim.utils.enums import FlightPhase, Config, SpeedMode, VerticalMode, APSpeedMode, APThrottleMode, APVerticalMode, APLateralMode
from airtrafficsim.core.traffic import Traffic


class Environment:
    """
    Base class for simulation environment

    """

    def __init__(self, file_name="default", start_time = datetime.utcnow(), end_time = 60, era5_weather=False, bada_perf=False):
        # User setting
        self.start_time = start_time
        """The simulation start time [datetime object]"""
        self.end_time = end_time
        """The simulation end time [s]"""

        # Simulation variable
        self.traffic = Traffic(file_name, start_time, end_time, era5_weather, bada_perf)
        self.global_time = 0                    # [s]

        # Handle io
        self.datetime = datetime.utcnow()
        self.last_sent_time = time.time()
        self.graph_type = 'None'
        self.packet_id = 0
        # Buffer
        self.buffer_time = []
        self.lat = []
        self.long = []
        self.alt = []
        self.cas = []

        # File IO
        self.file_name = file_name+'-'+self.datetime.isoformat(timespec='seconds')
        self.folder_path = Path(__file__).parent.parent.parent.resolve().joinpath('result/'+self.file_name)
        self.folder_path.mkdir()
        self.file_path =  self.folder_path.joinpath(self.file_name+'.csv')
        self.writer = csv.writer(open(self.file_path, 'w+'))
        self.header = ['timestep','timestamp', 'id', 'callsign', 'lat', 'long', 'alt',
                        'cas', 'tas', 'mach', 'vs', 
                        'heading', 'bank_angle', 'path_angle',
                        'mass', 'fuel_consumed', 
                        'thrust', 'drag', 'esf', 'accel',
                        'ap_track_angle', 'ap_heading', 'ap_alt', 'ap_cas', 'ap_mach', 'ap_procedural_speed', 
                        'ap_wp_index', 'ap_next_wp', 'ap_dist_to_next_fix', 'ap_holding_round', 
                        'flight_phase', 'configuration', 'speed_mode', 'vertical_mode','ap_speed_mode', 'ap_lateral_mode', 'ap_throttle_mode']
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

    def step(self, socketio=None):
        """
        Conduct one simulation timestep.
        """
        start_time = time.time()

        # Run atc command
        self.atc_command()
        # Run update loop
        self.traffic.update(self.global_time)
        # Save to file
        self.save()

        print("Environment - step() for global time", self.global_time, "/", self.end_time, "finished at", time.time() - start_time)
        
        if(socketio != None):
            # Save to buffer
            self.buffer_time.append((self.datetime + timedelta(seconds=self.global_time)).isoformat())
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
                self.buffer_time = []
                self.lat = []
                self.long = []
                self.alt = []
                self.cas = []

        self.global_time += 1

    def run(self, socketio=None):
        if socketio:
            socketio.emit('simulationEnvironment', {'header': self.header, 'file': self.file_name})

        for _ in range(self.end_time+1):
            # One timestep

            # Check if the simulation should end
            if self.should_end():
                self.end_time = self.global_time
                break

            self.step(socketio)
            
        print("")
        print("Export to CSVs")
        self.export_to_csv()
        print("")
        print("Simulation finished")


    def save(self):
        """
        Save all states variable of one timestemp to csv file.
        """
        data = np.column_stack((np.full(len(self.traffic.index), self.global_time), np.full(len(self.traffic.index), (self.start_time + timedelta(seconds=self.global_time)).isoformat(timespec='seconds')), self.traffic.index, self.traffic.call_sign, self.traffic.lat, self.traffic.long, self.traffic.alt,
                                self.traffic.cas, self.traffic.tas, self.traffic.mach, self.traffic.vs,
                                self.traffic.heading, self.traffic.bank_angle, self.traffic.path_angle,
                                self.traffic.mass, self.traffic.fuel_consumed,
                                self.traffic.perf.thrust, self.traffic.perf.drag, self.traffic.perf.esf, self.traffic.accel,
                                self.traffic.ap.track_angle, self.traffic.ap.heading, self.traffic.ap.alt, self.traffic.ap.cas, self.traffic.ap.mach, self.traffic.ap.procedure_speed ,
                                self.traffic.ap.flight_plan_index, [self.traffic.ap.flight_plan_name[i][val] if (val < len(self.traffic.ap.flight_plan_name[i])) else "NONE" for i, val in enumerate(self.traffic.ap.flight_plan_index)], self.traffic.ap.dist, self.traffic.ap.holding_round,  # autopilot variable
                                [FlightPhase(i).name for i in self.traffic.flight_phase], [Config(i).name for i in self.traffic.configuration], [SpeedMode(i).name for i in self.traffic.speed_mode], [VerticalMode(i).name for i in self.traffic.vertical_mode],
                                [APSpeedMode(i).name for i in self.traffic.ap.speed_mode], [APLateralMode(i).name for i in self.traffic.ap.lateral_mode], [APThrottleMode(i).name for i in self.traffic.ap.auto_throttle_mode])) # mode
        
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

        for i in range(len(self.traffic.index)):
            print(self.traffic.index)
            positions = np.column_stack((np.array(self.buffer_time, dtype="object"), long[:,i], lat[:,i], Unit.ft2m(alt[:, i]))).flatten().tolist()
            label = [{"interval": time+"/"+(self.start_time + timedelta(seconds=self.end_time)).isoformat(), 
                    "string": self.traffic.call_sign[i]+"\n"+str(np.floor(alt))+"ft "+str(np.floor(cas))+"kt"} 
                    for time, alt, cas in zip(self.buffer_time, alt[:,i], cas[:,i])]
            
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
        
