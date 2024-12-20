import csv
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from flask_socketio import SocketIO

import numpy as np
import pandas as pd

from ..types import array
from ..utils.enums import (
    APLateralMode,
    APSpeedMode,
    APThrottleMode,
    Config,
    FlightPhase,
    SpeedMode,
    VerticalMode,
)
from ..utils.unit_conversion import Unit
from .performance.performance import PerformanceMode
from .traffic import Traffic
from .weather.weather import WeatherMode


# FIXME(abrah): single responsibility principle - split this up.
class Environment:
    """
    Base class for simulation environment.
    inherit this to create a new simulation environment.
    """

    def __init__(
        self,
        file_name: str,
        start_time: datetime,
        duration_s: float,
        weather_mode: WeatherMode = "ISA",
        performance_mode: PerformanceMode = "BADA",
    ):
        # User setting
        self.start_time = start_time
        """The simulation start time [datetime object]"""
        self.duration_s = duration_s
        """The simulation duration [s]"""

        # Simulation variable
        self.traffic = Traffic(
            file_name, start_time, duration_s, weather_mode, performance_mode
        )
        self.seconds_since_start: float = 0.0  # [s]

        # Handle io
        self.datetime = datetime.now(timezone.utc)
        self.last_sent_time = time.time()
        self.graph_type = "None"
        self.packet_id = 0
        self.buffer_data: list[array] = []

        # File IO
        self.file_name = (
            file_name + "-" + self.datetime.isoformat(timespec="seconds")
        )
        self.folder_path = (
            Path(__file__)
            .parent.parent.resolve()
            .joinpath("data/result/" + self.file_name)
        )
        self.folder_path.mkdir()
        self.file_path = self.folder_path.joinpath(self.file_name + ".csv")
        self.writer = csv.writer(open(self.file_path, "w+"))
        self.header = [
            "timestep",
            "timestamp",
            "id",
            "callsign",
            "lat",
            "long",
            "alt",
            "cas",
            "tas",
            "mach",
            "vs",
            "heading",
            "bank_angle",
            "path_angle",
            "mass",
            "fuel_consumed",
            "thrust",
            "drag",
            "esf",
            "accel",
            "ap_track_angle",
            "ap_heading",
            "ap_alt",
            "ap_cas",
            "ap_mach",
            "ap_procedural_speed",
            "ap_wp_index",
            "ap_next_wp",
            "ap_dist_to_next_fix",
            "ap_holding_round",
            "flight_phase",
            "configuration",
            "speed_mode",
            "vertical_mode",
            "ap_speed_mode",
            "ap_lateral_mode",
            "ap_throttle_mode",
        ]
        self.writer.writerow(self.header)
        self.header.remove("timestep")
        self.header.remove("timestamp")
        self.header.remove("id")
        self.header.remove("callsign")

    # FIXME(abrah): use protocols instead
    def atc_command(self) -> None:
        """
        Virtual method to execute user command each timestep.
        """
        pass

    def should_end(self) -> bool:
        """
        Virtual method to determine whether the simulation should end each
        timestep.
        """
        return False

    def step(self, socketio: SocketIO | None = None) -> None:
        """
        Conduct one simulation timestep.
        """
        start_time = time.time()

        # Run atc command
        self.atc_command()
        # Run update loop
        self.traffic.update(self.seconds_since_start)
        # Save to file
        self.save()

        print(
            "Environment - step() for global time",
            self.seconds_since_start,
            "/",
            self.duration_s,
            "finished at",
            time.time() - start_time,
        )

        if socketio is not None:
            # Save to buffer
            data = np.column_stack(
                (
                    self.traffic.index,
                    self.traffic.call_sign,
                    np.full(
                        len(self.traffic.index),
                        (
                            self.start_time
                            + timedelta(seconds=self.seconds_since_start)
                        ).isoformat(timespec="seconds"),
                    ),
                    self.traffic.long,
                    self.traffic.lat,
                    Unit.ft2m(self.traffic.alt),
                    self.traffic.cas,
                )
            )
            self.buffer_data.extend(data)

            @socketio.on("setSimulationGraphType")  # type: ignore
            def set_simulation_graph_type(graph_type: str):
                self.graph_type = graph_type

            now = time.time()
            if ((now - self.last_sent_time) > 0.5) or (
                self.seconds_since_start == self.duration_s
            ):
                self.send_to_client(socketio)
                socketio.sleep(0)
                self.last_sent_time = now
                self.buffer_data = []

        self.seconds_since_start += 1

    def run(self, socketio: SocketIO | None = None) -> None:
        """
        Run the simulation for all timesteps.

        Parameters
        ----------
        socketio : socketio object, optional
            Socketio object to handle communciation when running simulation, by
            default None
        """
        if socketio:
            socketio.emit(
                "simulationEnvironment",
                {"header": self.header, "file": self.file_name},
            )

        # FIXME: are we sure we want \Delta t = 1s
        for _ in range(int(self.duration_s + 1)):
            # One timestep

            # Check if the simulation should end
            if self.should_end():
                self.duration_s = self.seconds_since_start
                break

            self.step(socketio)

        # print("")
        # print("Export to CSVs")
        # self.export_to_csv()
        print("")
        print("Simulation finished")

    def save(self) -> None:
        """
        Save all states variable of one timestemp to csv file.
        """
        data = np.column_stack(
            (
                np.full(len(self.traffic.index), self.seconds_since_start),
                np.full(
                    len(self.traffic.index),
                    (
                        self.start_time
                        + timedelta(seconds=self.seconds_since_start)
                    ).isoformat(timespec="seconds"),
                ),
                self.traffic.index,
                self.traffic.call_sign,
                self.traffic.lat,
                self.traffic.long,
                self.traffic.alt,
                self.traffic.cas,
                self.traffic.tas,
                self.traffic.mach,
                self.traffic.vs,
                self.traffic.heading,
                self.traffic.bank_angle,
                self.traffic.path_angle,
                self.traffic.mass,
                self.traffic.fuel_consumed,
                self.traffic.perf.thrust,
                self.traffic.perf.drag,
                self.traffic.perf.esf,
                self.traffic.accel,
                self.traffic.autopilot.track_angle,
                self.traffic.autopilot.heading,
                self.traffic.autopilot.alt,
                self.traffic.autopilot.cas,
                self.traffic.autopilot.mach,
                self.traffic.autopilot.procedure_speed,
                self.traffic.autopilot.flight_plan_index,
                [
                    self.traffic.autopilot.flight_plan_name[i][val]
                    if (val < len(self.traffic.autopilot.flight_plan_name[i]))
                    else "NONE"
                    for i, val in enumerate(
                        self.traffic.autopilot.flight_plan_index
                    )
                ],
                self.traffic.autopilot.dist,
                self.traffic.autopilot.holding_round,  # autopilot variable
                [FlightPhase(i).name for i in self.traffic.flight_phase],
                [Config(i).name for i in self.traffic.configuration],
                [SpeedMode(i).name for i in self.traffic.speed_mode],
                [VerticalMode(i).name for i in self.traffic.vertical_mode],
                [
                    APSpeedMode(i).name
                    for i in self.traffic.autopilot.speed_mode
                ],
                [
                    APLateralMode(i).name
                    for i in self.traffic.autopilot.lateral_mode
                ],
                [
                    APThrottleMode(i).name
                    for i in self.traffic.autopilot.auto_throttle_mode
                ],
            )
        )  # mode

        self.writer.writerows(data)

    # FIXME(abrah): allow custom path instead.
    def export_to_csv(self) -> None:
        """
        Export the simulation result to a csv file.
        """
        df = pd.read_csv(self.file_path)
        for id in df["id"].unique():
            df[df["id"] == id].to_csv(
                self.folder_path.joinpath(str(id) + ".csv"), index=False
            )
        # self.file_path.unlink()

    def send_to_client(self, socketio: SocketIO) -> None:
        """
        Send the simulation data to client.

        Parameters
        ----------
        socketio : socketio object
            socketio object to handle communciation when running simulation
        """
        print("send to client")

        document = [
            {
                "id": "document",
                "name": "simulation",
                "version": "1.0",
                "clock": {
                    "interval": self.start_time.isoformat()
                    + "/"
                    + (
                        self.start_time + timedelta(seconds=self.duration_s)
                    ).isoformat(),
                    "currentTime": self.start_time.isoformat(),
                },
            }
        ]

        df_buffer = pd.DataFrame(self.buffer_data)
        if self.buffer_data:
            for id in df_buffer.iloc[:, 0].unique():
                content = df_buffer[df_buffer.iloc[:, 0] == id]

                call_sign = content.iloc[0, 1]
                positions = (
                    content.iloc[:, [2, 3, 4, 5]].to_numpy().flatten().tolist()
                )
                label = [
                    {
                        "interval": time
                        + "/"
                        + (
                            self.start_time + timedelta(seconds=self.duration_s)
                        ).isoformat(),
                        "string": call_sign
                        + "\n"
                        + str(np.floor(Unit.m2ft(alt)))
                        + "ft "
                        + str(np.floor(cas))
                        + "kt",
                    }
                    for time, alt, cas in zip(
                        content.iloc[:, 2].to_numpy(),
                        content.iloc[:, 5].to_numpy(dtype=float),
                        content.iloc[:, 6].to_numpy(dtype=float),
                    )
                ]

                trajectory = {
                    "id": call_sign,
                    "position": {"cartographicDegrees": positions},
                    "point": {
                        "pixelSize": 5,
                        "color": {"rgba": [39, 245, 106, 215]},
                    },
                    "path": {
                        "leadTime": 0,
                        "trailTime": 20,
                        "distanceDisplayCondition": {
                            "distanceDisplayCondition": [0, 1500000]
                        },
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
                        "backgroundColor": {"rgba": [0, 0, 0, 50]},
                    },
                }
                document.append(trajectory)

        graph_data = []
        if self.graph_type != "None":
            df = pd.read_csv(self.file_path)
            for id in df["id"].unique():
                content = df[df["id"] == id]
                graph_data.append(
                    {
                        "x": content["timestep"].to_list(),
                        "y": content[self.graph_type].to_list(),
                        "name": content.iloc[0]["callsign"],
                        "type": "scattergl",
                        "mode": "lines",
                    }
                )

        socketio.emit(
            "simulationData",
            {
                "czml": document,
                "progress": self.seconds_since_start / self.duration_s,
                "packet_id": self.packet_id,
                "graph": graph_data,
            },
        )
        self.packet_id = self.packet_id + 1
