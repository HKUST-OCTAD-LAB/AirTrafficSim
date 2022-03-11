from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

class Replay:
    @staticmethod
    def get_replay_dir():
        """Return a list of directories in data/replay given path"""
        replay_list = []
        for dir in Path(__file__).parent.parent.parent.joinpath('data/replay/historic').iterdir():
            if dir.is_dir():
                replay_list.append(dir.name)
        
        simulation_list=[]
        for dir in Path(__file__).parent.parent.parent.joinpath('data/replay/simulation').iterdir():
            if dir.is_dir():
                simulation_list.append(dir.name)

        replay_list.sort(reverse=True)
        simulation_list.sort(reverse=True)
        return {"historic": replay_list, "simulation": simulation_list}


    @staticmethod
    def get_replay_czml(category, date):
        """Send CZML file of the replay date for visualization"""
        trajectories = []
        start_time = None
        end_time = None
        for file in Path(__file__).parent.parent.parent.joinpath('data/replay/',category,date).iterdir():
            file_content = pd.read_csv(file)
            start = file_content.iloc[0]['timestamp']
            end = file_content.iloc[-1]['timestamp']
            
            if start_time == None and end_time == None:
                start_time = start
                end_time = end

            if start < start_time:
                start_time = start

            if end > end_time:
                end_time = end
            
            positions =  np.column_stack((file_content['timestamp'].map(lambda x : datetime.utcfromtimestamp(x).isoformat()), 
                                    file_content['long'].values, file_content['lat'].values, file_content['alt'].values/3.2808)).flatten().tolist()
            label = [{"interval": datetime.utcfromtimestamp(time).isoformat()+"/"+datetime.utcfromtimestamp(end).isoformat(), 
                    "string": file.name+"\n"+str(alt)+"ft "+str(gspeed)+"kt"} 
                    for time, alt, gspeed in zip(file_content['timestamp'], file_content['alt'], file_content['gspeed'])]
            
            trajectory = {
                "id": file.name,
                "availability": datetime.utcfromtimestamp(start).isoformat()+"/"+ datetime.utcfromtimestamp(end).isoformat(),
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
                        "distanceDisplayCondition": [0, 1000000]
                    },
                    #     "resolution": 600.0,
                    #     "material": {
                    #     "polylineDash": {}
                    # }
                },
                "label": {
                    "text": label,
                    "font": "9px sans-serif",
                    "horizontalOrigin": "LEFT",
                    "pixelOffset": {
                        "cartesian2": [20, 20],
                    },
                    "distanceDisplayCondition": {
                        "distanceDisplayCondition": [0, 1000000]
                    },
                    "showBackground": "true",
                    "backgroundColor": {
                        "rgba": [0, 0, 0, 50]
                    }
                }
            }

            trajectories.append(trajectory);

        document = {
            "id": "document",
            "name": "Replay",
            "version": "1.0",
            "clock": {
                "interval": datetime.utcfromtimestamp(start_time).isoformat()+"/"+ datetime.utcfromtimestamp(end_time).isoformat(),
                "currentTime": datetime.utcfromtimestamp(start_time).isoformat()
            }
        }
        trajectories.insert(0, document)
        return trajectories
