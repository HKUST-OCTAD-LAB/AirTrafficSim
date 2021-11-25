import React, {useEffect, useRef } from "react";
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, IonImageryProvider, viewerCesiumInspectorMixin } from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef } from "resium";
import Aircrafts from "../components/Aircrafts";

Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = createWorldTerrain( {requestVertexNormals: true, requestWaterMask: true});
const SentinelTwoImagery = new IonImageryProvider({ assetId: 3954 }) //createWorldImagery() for Bing Imagery

const CesiumBase = () => {
    const viewerRef = useRef<CesiumComponentRef<CesiumViewer>>(null);

    useEffect(() => {
      console.log("useEffect() - Cesium Base")
        if (viewerRef.current && viewerRef.current.cesiumElement) {
          // ref.current.cesiumElement is Cesium's Viewer
          // DO SOMETHING
          console.log(viewerRef);
          viewerRef.current.cesiumElement.extend(viewerCesiumInspectorMixin)
        }
      }, []);

      
    return (
        <Viewer ref={viewerRef} style={{height: "100vh"}}  homeButton={false} baseLayerPicker={false} fullscreenButton={false} navigationHelpButton={false} imageryProvider={SentinelTwoImagery}>
            <Globe terrainProvider={terrainProvider} enableLighting={true}/>
            <Cesium3DTileset url={IonResource.fromAssetId(96188)}/>
            <Aircrafts/>
        </Viewer>
    )
};

export default CesiumBase;