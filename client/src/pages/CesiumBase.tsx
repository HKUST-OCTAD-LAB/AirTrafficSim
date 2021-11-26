import React, {useEffect, useRef } from "react";
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, IonImageryProvider, createWorldImagery } from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef, Camera, Scene } from "resium";
import Aircrafts from "../components/Aircrafts";

Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = createWorldTerrain();
const SentinelTwoImagery = new IonImageryProvider({ assetId: 3954 }); //createWorldImagery() for Bing Imagery
const bingImagery = createWorldImagery(); //createWorldImagery() for Bing Imagery

const CesiumBase = () => {
    const viewerRef = useRef<CesiumComponentRef<CesiumViewer>>(null);

    useEffect(() => {
      console.log("useEffect() - Cesium Base")
        if (viewerRef.current && viewerRef.current.cesiumElement) {
          // ref.current.cesiumElement is Cesium's Viewer
          // DO SOMETHING
        }
      }, []);

      
    return (
      <Viewer imageryProvider={bingImagery} ref={viewerRef} style={{height: "100vh"}}  homeButton={false} baseLayerPicker={false} fullscreenButton={false} navigationHelpButton={false}>
        <Scene debugShowFramesPerSecond={true}/>
        <Globe terrainProvider={terrainProvider}/>
        <Cesium3DTileset url={IonResource.fromAssetId(96188)}/>
        {/* <Camera onChange={(res) => {
          console.log("camera change: ", res);
          if (viewerRef.current && viewerRef.current.cesiumElement){
            onCameraChange(viewerRef.current.cesiumElement);
          }
        }}/> */}
        <Aircrafts/>
      </Viewer>
    )
};

const onCameraChange = (viewer:CesiumViewer) => {
    console.log(viewer);
    var currentMagnitude = viewer.camera.getMagnitude();
    console.log('current magnitude - ', currentMagnitude);
    var direction = viewer.camera.direction;
    console.log("camera direction", direction.x, direction.y, direction.z);
    var rectangle = viewer.camera.computeViewRectangle();
    console.log("camera rectangle", rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180, rectangle!.south/Math.PI*180);
}

export default CesiumBase;