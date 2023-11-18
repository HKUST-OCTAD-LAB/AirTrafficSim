import React, { useState, useEffect, useContext, useRef, useCallback } from "react";
import { CesiumContext } from "./CesiumContext";
import {
    Ion, IonResource, Viewer as CesiumViewer,
    createWorldTerrainAsync, createWorldImageryAsync,
    OpenStreetMapImageryProvider, MapboxStyleImageryProvider, // WebMapServiceImageryProvider
    Cesium3DTileStyle, CzmlDataSource as cesiumCzmlDataSource,
    Color, JulianDate, HeadingPitchRange,
} from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef, Scene, ImageryLayer, Clock, Camera } from "resium";
import Plot from 'react-plotly.js';
import socket from "../utils/websocket"

import './Simulation.scss';

Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = await createWorldTerrainAsync();
const osmBuilding = IonResource.fromAssetId(96188);
const osmBuildingstyle = new Cesium3DTileStyle({
    color: 'color("grey")'
});
const bingImagery = await createWorldImageryAsync();
const simpleImagery = new OpenStreetMapImageryProvider({ url: 'https://stamen-tiles.a.ssl.fastly.net/toner-background/' });
// const mapboxImagery = new MapboxStyleImageryProvider({
//     styleId: 'dark-v10',
//     accessToken: process.env.REACT_APP_MAPBOX_ACCESS_TOKEN!
// });

const replayDataSource = new cesiumCzmlDataSource();
const simulationDataSource = new cesiumCzmlDataSource();
const navDataSource = new cesiumCzmlDataSource();
const era5WindDataSource = new cesiumCzmlDataSource();
const era5RainDataSource = new cesiumCzmlDataSource();
const radarImageDataSource = new cesiumCzmlDataSource();

const defaultZoom = new HeadingPitchRange(0, -90, 500000);

const Simulation: React.FC = () => {
    const [viewerRef, setViewerRef] = useState<CesiumComponentRef<CesiumViewer> | null>(null);

    const handleRef = useCallback((ref: CesiumComponentRef<CesiumViewer> | null) => {
        if (ref && ref.cesiumElement && !viewerRef) {
            console.log("ref", ref);
            setViewerRef(ref);
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
            />
            {/* <Globe
                baseColor={Color.fromCssColorString("#000000")}
                terrainProvider={terrainProvider}
                showGroundAtmosphere={false}
            /> */}
            {/* <div id="panel">
                {viewerRef ? <Panel /> : "Loading..."}
            </div> */}
        </main>
    </CesiumContext.Provider>
};

const Panel = () => {
    const { viewerRef } = useContext(CesiumContext);

    console.log("component1 rendered", viewerRef);

    return <div>Component1</div>;
};

export default Simulation;
