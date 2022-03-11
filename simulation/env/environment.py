from socket import socket
import time
from flask_socketio import emit
from datetime import datetime, timedelta
import numpy as np

from utils.enums import Flight_phase
from utils.unit import Unit_conversion
from traffic.traffic import Traffic
from traffic.aircraft import Aircraft


class Environment:

    def __init__(self, socket=False):

        self.global_time = 0                    # [s]
        self.end_time = 10000                    # [s]

        self.time_to_target = 0                 # [s]

        self.traffic = Traffic('simulation', 2)
        self.aircraft_head = Aircraft(self.traffic, "HEAD", "A20N", Flight_phase.CRUISE, 22.387778, 113.428116, 20000.0, 175.0, 310.0, 10000.0, 12000.0, ["SIERA", "CANTO", "MURRY", "GOODI", "SILVA", "LIMES"])
        self.aircraft_fol = Aircraft(self.traffic, "FOLLOW", "A20N", Flight_phase.CRUISE, 21.9, 113.5, 20000.0, 175.0, 310.0, 10000.0, 12000.0)

        # Handle io
        self.socket = socket                    # Whether to send message to client through socket
        self.datetime = datetime.utcnow()
        self.last_sent_time = time.time()

        # Buffer
        self.time = []
        self.lat = []
        self.long = []
        self.alt = []
        self.cas = []

        

    def run(self):
        for i in range(self.end_time):
            self.step()


    def step(self):
        start_time = time.time()
        print("")
        print("Environment - step(), time = ", self.global_time)
        print("")
        print("Set ATC command")
        if self.global_time == 10:  
            # Right
            self.aircraft_fol.set_heading(220)
            # Left
            # self.aircraft_head.set_heading(150)

        if self.global_time == 100:
            # Climb
            self.aircraft_fol.set_alt(10000)
            # Descend
            self.aircraft_head.set_alt(30000)

        if self.global_time == 300:
            # Accelerate
            self.aircraft_fol.set_speed(200)
            # self.aircraft_head.set_mach(0.7)

        print("update states")
        self.traffic.update()
        print("Save to file")
        self.traffic.save(self.global_time)
        
        if(socket):
            # Save to buffer
            self.time.append((self.datetime + timedelta(seconds=self.global_time)).isoformat())
            self.lat.append(self.traffic.lat)
            self.long.append(self.traffic.long)
            self.alt.append(self.traffic.alt)
            self.cas.append(self.traffic.cas)

            now = time.time()
            if ((now - self.last_sent_time) > 1) or (self.global_time == (self.end_time-1)):
                self.send_to_client()
                self.last_sent_time = now
                self.time = []
                self.lat = []
                self.long = []
                self.alt = []
                self.cas = []

        self.global_time += 1

        print("Environment - step() finish at", time.time() - start_time)


    def send_to_client(self):
        print("send to client")
        if self.global_time == 0:
            document = [{
                    "id": "document",
                    "name": "simulation",
                    "version": "1.0",
                    "clock": {
                        "interval": self.datetime.isoformat()+"/"+(self.datetime + timedelta(seconds=self.end_time)).isoformat(),
                        "currentTime": self.datetime.isoformat(),
                    }
                }]
        else:
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
        
        emit('simulationData',document)
        
