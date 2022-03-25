from locale import D_FMT
from pathlib import Path
import csv
import pandas as pd
import numpy as np
from datetime import datetime
from itertools import cycle

class Replay:
    @staticmethod
    def get_replay_dir():
        """Return a list of directories in data/replay given path"""
        historic_list = []
        for dir in Path(__file__).parent.parent.parent.joinpath('data/replay/historic').iterdir():
            if dir.is_dir():
                historic_list.append(dir.name)
        
        simulation_list=[]
        for dir in Path(__file__).parent.parent.parent.joinpath('data/replay/simulation').iterdir():
            if dir.is_dir():
                simulation_list.append(dir.name)

        historic_list.sort(reverse=True)
        simulation_list.sort(reverse=True)
        return {"historic": historic_list, "simulation": simulation_list}


    @staticmethod
    def get_replay_czml(replayCategory, replayFile):
        """Send CZML file of the file name for visualization"""
        trajectories = []
        start_time = None
        end_time = None
        for file in Path(__file__).parent.parent.parent.joinpath('data/replay/',replayCategory,replayFile).iterdir():
            if file != Path(__file__).parent.parent.parent.joinpath('data/replay/', replayCategory, replayFile, replayFile+'.csv'):
                file_content = pd.read_csv(file)
                
                if replayCategory == 'historic':
                    start = datetime.utcfromtimestamp(file_content.iloc[0]['timestamp'])
                    end = datetime.utcfromtimestamp(file_content.iloc[-1]['timestamp'])

                    id = file.name
                    positions =  np.column_stack((file_content['timestamp'].map(lambda x : datetime.utcfromtimestamp(x).isoformat()), 
                                            file_content['long'].values, file_content['lat'].values, file_content['alt'].values/3.2808)).flatten().tolist()
                    label = [{"interval": datetime.utcfromtimestamp(time).isoformat()+"/"+end.isoformat(), 
                            "string": file.name+"\n"+str(alt)+"ft "+str(gspeed)+"kt"} 
                            for time, alt, gspeed in zip(file_content['timestamp'], file_content['alt'], file_content['gspeed'])]
                
                elif replayCategory == 'simulation':
                    start = datetime.fromisoformat(file_content.iloc[0]['timestamp'])
                    end = datetime.fromisoformat(file_content.iloc[-1]['timestamp'])

                    id = file_content.iloc[0]['callsign']
                    positions =  np.column_stack((file_content['timestamp'], file_content['long'].values, file_content['lat'].values, file_content['alt'].values/3.2808)).flatten().tolist()
                    label = [{"interval": time+"/"+end.isoformat(), 
                            "string": id+"\n"+str(int(np.round(alt)))+"ft "+str(int(np.round(cas)))+"kt"} 
                            for time, alt, cas in zip(file_content['timestamp'], file_content['alt'], file_content['cas'])]
                

                if start_time == None and end_time == None:
                    start_time = start
                    end_time = end

                if start < start_time:
                    start_time = start

                if end > end_time:
                    end_time = end


                trajectory = {
                    "id": id,
                    "availability": start.isoformat()+"/"+ end.isoformat(),
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

        trajectories.insert(0, {
            "id": "document",
            "name": "Replay",
            "version": "1.0",
            "clock": {
                "interval": start_time.isoformat()+"/"+ end_time.isoformat(),
                "currentTime": start_time.isoformat(),
            }
        })
        return trajectories


    @staticmethod
    def get_graph_header(mode, replayCategory, replayFile):
        header = ['None']
        if mode == 'replay' and replayCategory == 'simulation':
            header.extend(next(csv.reader(open(next(Path(__file__).parent.parent.parent.joinpath('data/replay/',replayCategory,replayFile).glob('*.csv'))))))
            header.remove('timestep')
            header.remove('timestamp')
            header.remove('id')
            header.remove('callsign')
            header.remove('lat')
            header.remove('long')
        return header

    @staticmethod
    def get_graph_data(mode, replayCategory, replayFile, simulationFile, graph):
        data = []
        color = cycle(["#ea5545", "#f46a9b", "#ef9b20", "#edbf33", "#ede15b", "#bdcf32", "#87bc45", "#27aeef", "#b33dc6"])
        if mode == 'replay' and replayCategory == 'simulation' and graph != 'None':
            for file in Path(__file__).parent.parent.parent.joinpath('data/replay/',replayCategory,replayFile).iterdir():
                if file != Path(__file__).parent.parent.parent.joinpath('data/replay/', replayCategory, replayFile, replayFile+'.csv'):
                    df = pd.read_csv(file)
                    data.append({
                        "name": df.iloc[0]['callsign'],
                        "color": next(color),
                        "data": [{"time": time, 
                                "value": graph} 
                                for time, graph in zip(df['timestep'], df[graph])]
                    })
                
        elif mode == 'simulation' and graph != 'None':
            df = pd.read_csv(Path(__file__).parent.parent.parent.joinpath('data/replay/simulation',simulationFile,simulationFile+'.csv'))
            for id in df['id'].unique():
                content = df[df['id'] == id]
                data.append({
                    "name": content.iloc[0]['callsign'],
                    "color": next(color),
                    "data": [{"time": time, 
                              "value": graph} 
                              for time, graph in zip(content['timestep'], content[graph])]
                })  

        return data
