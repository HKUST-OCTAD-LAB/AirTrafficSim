import { useState, useContext, useCallback } from "react";
import { CesiumContext } from "./context/CesiumContext";
import * as Cesium from 'cesium';
import { Viewer, CesiumComponentRef, ImageryLayer } from "resium";
import { socket } from "./socket";
import { Button } from '@carbon/react';

import './App.scss';

Cesium.Ion.defaultAccessToken = import.meta.env.VITE_CESIUMION_ACCESS_TOKEN!;
const bingImagery = Cesium.Ion.defaultAccessToken ? await Cesium.createWorldImageryAsync() : undefined;
const terrainProvider = Cesium.Ion.defaultAccessToken ? await Cesium.createWorldTerrainAsync() : undefined;
const osmBuilding = Cesium.Ion.defaultAccessToken ? await Cesium.createOsmBuildingsAsync({
    style: new Cesium.Cesium3DTileStyle({ color: 'color("grey")' })
}) : undefined;
const dataSources = {
    replay: new Cesium.CzmlDataSource(),
    simulation: new Cesium.CzmlDataSource(),
    nav: new Cesium.CzmlDataSource(),
    era5Wind: new Cesium.CzmlDataSource(),
    era5Rain: new Cesium.CzmlDataSource(),
    radarImage: new Cesium.CzmlDataSource(),
}

const App = () => {
    const [viewerRef, setViewerRef] = useState<CesiumComponentRef<Cesium.Viewer> | null>(null);
    const [connected, setConnected] = useState<boolean>(false);

    const handleRef = useCallback((ref: CesiumComponentRef<Cesium.Viewer> | null) => {
        if (ref && ref.cesiumElement && !viewerRef) {
            setViewerRef(ref);
            ref.cesiumElement.scene.primitives.add(osmBuilding);
            ref.cesiumElement.dataSources.add(dataSources.replay);
            ref.cesiumElement.dataSources.add(dataSources.simulation);
            ref.cesiumElement.dataSources.add(dataSources.nav);
            ref.cesiumElement.dataSources.add(dataSources.era5Wind);
            ref.cesiumElement.dataSources.add(dataSources.era5Rain);
            ref.cesiumElement.dataSources.add(dataSources.radarImage);

            setConnected(socket.connected);
            socket.on("connect", () => {
                setConnected(true);
                console.log("connected");
            });
            socket.on("disconnect", () => setConnected(false));
            // socket.on("simulation_data", msg => {
            //     console.log("simulation_data", msg);
            // });
            // socket.on("simulation_env", msg => {
            //     console.log("simulation_env", msg);
            // });
            // socket.on("loading_msg", msg => {
            //     console.log("loading_msg", msg);
            // });
        }
    }, [viewerRef]);

    return <CesiumContext.Provider value={{ viewerRef: viewerRef, connected: connected }}>
        <main>
            <Viewer
                id="map"
                ref={handleRef}
                animation={false}
                timeline={false}
                selectionIndicator={false}
                homeButton={false}
                baseLayerPicker={false}
                sceneModePicker={false}
                fullscreenButton={false}
                navigationHelpButton={false}
                geocoder={false}
                terrainProvider={terrainProvider}
            >
                <ImageryLayer imageryProvider={bingImagery!} />
            </Viewer>

            <div id="panel">
                {viewerRef ? <Panel /> : "Loading..."}
            </div>
        </main>
    </CesiumContext.Provider>
};

const Panel = () => {
    const { viewerRef, connected } = useContext(CesiumContext);
    // const [timeNow, setTimeNow] = useState<number>(0);
    // const [timeStart, setTimeStart] = useState<number>(0);
    // const [timeStop, setTimeStop] = useState<number>(0);
    // const [timeSpeed, setTimeSpeed] = useState<number>(0);

    const getReplayDirs = () => {
        console.log("get_replay_dirs");
    }

    const getReplayCZML = (file: string) => {
        console.log("get_replay_czml", file);
    }

    const getGraphHeader = (graph_type: string) => {
        console.log("get_graph_header");
    }

    const getGraphData = () => {
        console.log("get_graph_data");
    }

    const getSimulationFile = () => {
        console.log("get_simulation_file");
    }

    const runSimulation = () => {
        console.log("run_simulation");
    }

    const clearData = () => {
        dataSources.replay.entities.removeAll();
        dataSources.simulation.entities.removeAll();
    }

    const getNav = () => {
        console.log("get_nav");
    }

    const getERA5Wind = () => {
        console.log("get_era5_wind");
    }
    
    const getEra5Rain = () => {
        console.log("get_era5_rain");
    }

    const getRadarImage = () => {
        console.log("get_radar_image");
    }

    return <div>
        <div>AirTrafficSim ({connected ? "CONNECTED" : "DISCONNECTED"})</div>
        <div>
            <Button size="sm">Test</Button>
        </div>
    </div>
};

export default App;
