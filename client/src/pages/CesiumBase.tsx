import React, {useRef } from "react";
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, IonImageryProvider, viewerCesiumInspectorMixin } from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef } from "resium";

Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = createWorldTerrain( {requestVertexNormals: true, requestWaterMask: true});
const SentinelTwoImagery = new IonImageryProvider({ assetId: 3954 }) //createWorldImagery() for Bing Imagery

const CesiumBase = () => {
    const viewer = useRef<CesiumComponentRef<CesiumViewer>>(null);;

    return (
        <Viewer ref={viewer} style={{height: "100vh"}} animation={false} homeButton={false} baseLayerPicker={false} fullscreenButton={false} navigationHelpButton={false} imageryProvider={SentinelTwoImagery}>
            <Globe terrainProvider={terrainProvider} enableLighting={true}/>
            <Cesium3DTileset url={IonResource.fromAssetId(96188)}/>
            {console.log(viewer)}
            {viewer?.current?.cesiumElement?.extend(viewerCesiumInspectorMixin)}
        </Viewer>
    )
};

export default CesiumBase;