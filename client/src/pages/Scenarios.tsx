import React, {useEffect, useRef, useState} from "react";
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, IonImageryProvider, createWorldImagery} from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef, Scene, CzmlDataSource } from "resium";
import axios from "axios";

Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = createWorldTerrain();
const SentinelTwoImagery = new IonImageryProvider({ assetId: 3954 }); //createWorldImagery() for Bing Imagery
const bingImagery = createWorldImagery(); //createWorldImagery() for Bing Imagery

const Scenarios = () => {
    const viewerRef = useRef<CesiumComponentRef<CesiumViewer>>(null);
    const [replay, setReplay] = useState();
    const [navData, setNavdata] = useState();

    useEffect(() => {
      console.log("useEffect() - Scenarios | page load - axios get")

      // axios.get("http://localhost:5000/replay").then( res => {
      //     console.log("replay", res.data);
      //     setReplay(res.data);
      // }).catch(err => {
      //     console.log(err);
      // })

      axios.get("http://localhost:5000/navdata").then( res => {
        console.log("navdata", res.data);
        setNavdata(res.data);
      }).catch(err => {
        console.log(err);
      })
    }, []);
      
    return (
      <Viewer imageryProvider={bingImagery} ref={viewerRef} style={{height: "100vh"}}  homeButton={false} baseLayerPicker={false} fullscreenButton={false} navigationHelpButton={false}>
        <Scene debugShowFramesPerSecond={true}/>
        <Globe terrainProvider={terrainProvider}/>
        <Cesium3DTileset url={IonResource.fromAssetId(96188)}/>
        {replay && <CzmlDataSource data={replay} onLoad={(ds) => {
            console.log(ds);
        }}/>}
        {navData && <CzmlDataSource data={navData} onLoad={(ds) => {
            console.log(ds);
        }}/>}
      </Viewer>
    )
};

export default Scenarios;