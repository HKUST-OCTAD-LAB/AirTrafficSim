from pathlib import Path
import csv
import pandas as pd
import numpy as np
from datetime import datetime, timezone


class Replay:
    @staticmethod
    def get_replay_dir():
        """
        Return a list of historic/simulation data directories in data/replay

        Returns
        -------
        {}
            JSON file of historic file list and simulation file list in data/replay directory
        """
        historic_list = []
        for dir in Path(__file__).parent.parent.parent.joinpath('data/flight_data').iterdir():
            if dir.is_dir():
                historic_list.append(dir.name)

        simulation_list = []
        simulation_file_list = {}
        for dir in Path(__file__).parent.parent.parent.joinpath('data/result').iterdir():
            if dir.is_dir():
                simulation_list.append(dir.name)
                file_list = []
                for file in dir.iterdir():
                    if file.is_file():
                        file_list.append(file.name)
                simulation_file_list[dir.name] = file_list

        historic_list.sort(reverse=True)
        simulation_list.sort(reverse=True)
        return {"historic": historic_list, "simulation": simulation_list, "simulation_files": simulation_file_list}

    @staticmethod
    def get_replay_czml(replayCategory, replayFile):
        """
        Generate CZML file for visualization given replay file name.

        Parameters
        ----------
        replayCategory : string
            The category to replay (historic / simulation)

        replayFile : string
            Name of the replay file directory

        Returns
        -------
        {}
            JSON CZML file
        """
        if replayCategory == 'historic':
            trajectories = []
            start_time = None
            end_time = None
            for file in Path(__file__).parent.parent.parent.joinpath('data/flight_data/', replayFile).iterdir():
                if file != Path(__file__).parent.parent.parent.joinpath('data/flight_data/', replayFile, replayFile+'.csv'):
                    file_content = pd.read_csv(file)

                    if replayCategory == 'historic':
                        # start = datetime.utcfromtimestamp(file_content.iloc[0]['timestamp'])
                        # end = datetime.utcfromtimestamp(file_content.iloc[-1]['timestamp'])

                        id = file.name
                        if ('timestamp' and 'long' and 'lat' and 'alt' and 'gspeed') in file_content:
                            # FR24
                            start = datetime.fromtimestamp(
                                file_content.iloc[0]['timestamp'], timezone.utc)
                            end = datetime.fromtimestamp(
                                file_content.iloc[-1]['timestamp'], timezone.utc)
                            positions = np.column_stack((file_content['timestamp'].map(lambda x: datetime.fromtimestamp(x, timezone.utc).isoformat()),
                                                         file_content['long'].values, file_content['lat'].values, file_content['alt'].values/3.2808)).flatten().tolist()
                            label = [{"interval": datetime.fromtimestamp(time, timezone.utc).isoformat()+"/"+end.isoformat(),
                                      "string": file.name+"\n"+str(alt)+"ft "+str(gspeed)+"kt"}
                                     for time, alt, gspeed in zip(file_content['timestamp'], file_content['alt'], file_content['gspeed'])]

                        elif ('timestamp' and 'longitude' and 'latitude' and 'altitude' and 'groundspeed') in file_content:
                            # Opensky
                            start = datetime.fromisoformat(
                                file_content.iloc[0]['timestamp']+'+00:00')
                            end = datetime.fromisoformat(
                                file_content.iloc[-1]['timestamp']+'+00:00')
                            positions = np.column_stack((file_content['timestamp'].map(lambda x: datetime.fromisoformat(x+'+00:00').isoformat(timespec='seconds')),
                                                         file_content['longitude'].values, file_content['latitude'].values, file_content['altitude'].values/3.2808))[::360].flatten().tolist()
                            label = [{"interval": datetime.fromisoformat(time+'+00:00').isoformat(timespec='seconds')+"/"+end.isoformat(timespec='seconds'),
                                      "string": file.name+"\n"+str(alt)+"ft "+str(gspeed)+"kt"}
                                     for time, alt, gspeed in zip(file_content['timestamp'], file_content['altitude'], file_content['groundspeed'])]
                            label = label[0::60]

                        # positions =  np.column_stack((file_content['timestamp'].map(lambda x : datetime.utcfromtimestamp(x).isoformat()),
                        #                         file_content['long'].values, file_content['lat'].values, file_content['alt'].values/3.2808)).flatten().tolist()
                        # label = [{"interval": datetime.utcfromtimestamp(time).isoformat()+"/"+end.isoformat(),
                        #         "string": file.name+"\n"+str(alt)+"ft "+str(gspeed)+"kt"}
                        #         for time, alt, gspeed in zip(file_content['timestamp'], file_content['alt'], file_content['gspeed'])]

                    if start_time == None and end_time == None:
                        start_time = start
                        end_time = end

                    if start < start_time:
                        start_time = start

                    if end > end_time:
                        end_time = end

                    trajectory = {
                        "id": id,
                        "availability": start.isoformat(timespec='seconds')+"/" + end.isoformat(timespec='seconds'),
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
                            "showBackground": True,
                            "backgroundColor": {
                                "rgba": [0, 0, 0, 50]
                            }
                        }
                    }
                    trajectories.append(trajectory)
            trajectories.insert(0, {
                "id": "document",
                "name": "Replay",
                "version": "1.0",
                "clock": {
                    "interval": start_time.isoformat(timespec='seconds')+"/" + end_time.isoformat(timespec='seconds'),
                    "currentTime": start_time.isoformat(timespec='seconds'),
                }
            })
            return trajectories

        elif replayCategory == 'simulation':
            df = pd.read_csv(
                Path(__file__).parent.parent.parent.joinpath('data/result', replayFile))
            document = [{
                "id": "document",
                "name": "simulation",
                "version": "1.0",
                "clock": {
                    "interval": df.iloc[0]['timestamp']+"/"+df.iloc[-1]['timestamp'],
                    "currentTime": df.iloc[0]['timestamp'],
                }
            }]

            for id in df['id'].unique():
                content = df[df['id'] == id]
                id = content.iloc[0]['callsign']
                positions = np.column_stack(
                    (content['timestamp'], content['long'].values, content['lat'].values, content['alt'].values/3.2808)).flatten().tolist()
                label = [{"interval": time+"/"+content.iloc[-1]['timestamp'],
                          "string": id+"\n"+str(int(np.round(alt)))+"ft "+str(int(np.round(cas)))+"kt"}
                         for time, alt, cas in zip(content['timestamp'], content['alt'], content['cas'])]
                document.append(
                    {
                        "id": id,
                        "availability": content.iloc[0]['timestamp']+"/" + content.iloc[-1]['timestamp'],
                        "position": {
                            "cartographicDegrees": positions
                        },
                        "point": {
                            "pixelSize": 5,
                            "color": {
                                "rgba": [39, 245, 106, 215]
                            }
                        },
                        # "billboard": {
                        #     "image":{
                        #         "interval": content.iloc[0]['timestamp']+"/"+ content.iloc[-1]['timestamp'],
                        #         "uri": "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iOTYiIGhlaWdodD0iOTYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHhtbDpzcGFjZT0icHJlc2VydmUiIG92ZXJmbG93PSJoaWRkZW4iPjxkZWZzPjxjbGlwUGF0aCBpZD0iY2xpcDAiPjxyZWN0IHg9IjU5MiIgeT0iMzEyIiB3aWR0aD0iOTYiIGhlaWdodD0iOTYiLz48L2NsaXBQYXRoPjwvZGVmcz48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDApIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtNTkyIC0zMTIpIj48cGF0aCBkPSJNNjc0IDM3OCA2NzQgMzY5IDY0NSAzNDguNSA2NDUgMzI5QzY0NSAzMjUuMSA2NDMgMzIwIDY0MCAzMjAgNjM3LjEgMzIwIDYzNSAzMjUuMSA2MzUgMzI5TDYzNSAzNDguNSA2MDYgMzY5IDYwNiAzNzggNjM1IDM2My41IDYzNSAzODUuMyA2MjUgMzk0IDYyNSA0MDAgNjQwIDM5NCA2NTUgNDAwIDY1NSAzOTQgNjQ1IDM4NS4zIDY0NSAzNjMuNSA2NzQgMzc4WiIgZmlsbD0iIzAwQ0MzMyIvPjwvZz48L3N2Zz4="
                        #     },
                        #     "scale": 1.0,
                        #     # "rotation": 1.3,
                        #     "alignedAxis": {
                        #         "velocityReference": id+"#position"
                        #     }
                        # },
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
                            "showBackground": True,
                            "backgroundColor": {
                                "rgba": [0, 0, 0, 50]
                            }
                        }
                    }
                )
            return document

    @staticmethod
    def get_graph_header(mode, replayCategory, replayFile):
        """
        Get the list of parameters name of a file suitable for plotting graph.

        Parameters
        ----------
        mode : string
            AirTrafficSim mode (replay / simulation)
        replayCategory : string
            The category to replay (historic / simulation)
        replayFile : string
            Name of the replay file directory

        Returns
        -------
        string[]
            List of graph headers
        """
        header = ['None']
        if mode == 'replay' and replayCategory == 'simulation':
            with open(Path(__file__).parent.parent.parent.joinpath('data/result', replayFile), 'r') as file:
                header.extend(next(csv.reader(file)))
            header.remove('timestep')
            header.remove('timestamp')
            header.remove('id')
            header.remove('callsign')
            header.remove('lat')
            header.remove('long')
        return header

    @staticmethod
    def get_graph_data(mode, replayCategory, replayFile, simulationFile, graph):
        """
        Get the data for the selected parameters to plot a graph.

        Parameters
        ----------
        mode : string
            AirTrafficSim mode (replay / simulation)
        replayCategory : string
            The category to replay (historic / simulation)
        replayFile : string
            Name of the replay file directory

        Returns
        -------
        {}
            JSON file for graph data for Plotly.js
        """
        data = []
        if mode == 'replay' and replayCategory == 'simulation' and graph != 'None':
            df = pd.read_csv(
                Path(__file__).parent.parent.parent.joinpath('data/result/', replayFile))
            for id in df['id'].unique():
                content = df[df['id'] == id]
                data.append({
                    "x": content['timestep'].to_list(),
                    "y": content[graph].to_list(),
                    "name": content.iloc[0]['callsign'],
                    "type": 'scattergl',
                    "mode": 'lines',
                })

        elif mode == 'simulation' and graph != 'None':
            df = pd.read_csv(Path(__file__).parent.parent.parent.joinpath(
                'data/result/', simulationFile, simulationFile+'.csv'))
            for id in df['id'].unique():
                content = df[df['id'] == id]
                data.append({
                    "x": content['timestep'].to_list(),
                    "y": content[graph].to_list(),
                    "name": content.iloc[0]['callsign'],
                    "type": 'scattergl',
                    "mode": 'lines',
                })

        return data
