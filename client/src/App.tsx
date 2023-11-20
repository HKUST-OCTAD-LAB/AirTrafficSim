import { useState, useContext, useCallback } from "react";
import { CesiumContext } from "./context/CesiumContext";
import * as Cesium from 'cesium';
import { Viewer, CesiumComponentRef, ImageryLayer } from "resium";

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

// time {
    // start: number
    // stop: number
    // now: number
// }

const App = () => {
    const [viewerRef, setViewerRef] = useState<CesiumComponentRef<Cesium.Viewer> | null>(null);
    const [timeStart, setTimeStart] = useState<number>(0);
    const [timeStop, setTimeStop] = useState<number>(0);
    const [timeNow, setTimeNow] = useState<number>(0);


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
        }
    }, [viewerRef]);

    return <CesiumContext.Provider value={{ viewerRef: viewerRef }}>
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
    const { viewerRef } = useContext(CesiumContext);
    const [connected, setConnected] = useState<boolean>(false);

    console.log("component1 rendered", viewerRef);

    return <div>Component1</div>;
};

export default App;
