import React, {useEffect, useRef } from "react";
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, IonImageryProvider, createWorldImagery, CzmlDataSource, OpenStreetMapImageryProvider, Color} from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef, Scene, ImageryLayer } from "resium";
import socket from "../utils/websocket";
import axios from "axios";

Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = createWorldTerrain();
const SentinelTwoImagery = new IonImageryProvider({ assetId: 3954 }); //createWorldImagery() for Bing Imagery
const bingImagery = createWorldImagery(); //createWorldImagery() for Bing Imagery
const simple = new OpenStreetMapImageryProvider({url: 'https://stamen-tiles.a.ssl.fastly.net/toner-background/' });

const Simulation = () => {
    const viewerRef = useRef<CesiumComponentRef<CesiumViewer>>(null);

    useEffect(() => {
      console.log("useEffect() - Cesium Base")

      axios.get("http://localhost:5000/api/simulation").then( res => {
          console.log("replay", res.data);
      }).catch(err => {
          console.log(err);
      })

      if (viewerRef.current && viewerRef.current.cesiumElement) {
        // ref.current.cesiumElement is Cesium's Viewer
        // DO SOMETHING
        console.log("realtime");
        const viewer = viewerRef.current.cesiumElement;
        var czmldatasource = new CzmlDataSource();
        viewer.dataSources.add(czmldatasource);
        socket.on('simulation:all', (msg) => {
            console.log("simulation time data received");
            czmldatasource.process(msg);
        })
      }
  }, []);

      
    return (
      <Viewer imageryProvider={false} ref={viewerRef} style={{height: "100vh"}}  homeButton={false} baseLayerPicker={false} fullscreenButton={false} navigationHelpButton={false} skyAtmosphere={false}>
        <Scene debugShowFramesPerSecond={true}/>
        <Globe terrainProvider={terrainProvider} baseColor={Color.fromCssColorString('#000000')}/>
        {/* <ImageryLayer imageryProvider={simple} alpha={0.2}/> */}
        <ImageryLayer imageryProvider={simple} alpha={0.2} contrast={-1}/>
        <Cesium3DTileset url={IonResource.fromAssetId(96188)}/>
        {/* <Camera onChange={(res) => {
          console.log("camera change: ", res);
          if (viewerRef.current && viewerRef.current.cesiumElement){
            onCameraChange(viewerRef.current.cesiumElement);
          }
        }}/> */}
      </Viewer>
    )
};

// const onCameraChange = (viewer:CesiumViewer) => {
//     console.log(viewer);
//     var currentMagnitude = viewer.camera.getMagnitude();
//     console.log('current magnitude - ', currentMagnitude);
//     var direction = viewer.camera.direction;
//     console.log("camera direction", direction.x, direction.y, direction.z);
//     var rectangle = viewer.camera.computeViewRectangle();
//     console.log("camera rectangle", rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180, rectangle!.south/Math.PI*180);
// }

export default Simulation;