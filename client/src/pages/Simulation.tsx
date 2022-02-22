import React, {useEffect, useRef, useState } from "react";
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, IonImageryProvider, createWorldImagery, OpenStreetMapImageryProvider, Color, JulianDate} from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef, Scene, ImageryLayer, CzmlDataSource, Clock } from "resium";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend, ReferenceLine, CartesianGrid } from "recharts";
import Stack from "@mui/material/Stack";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Select from "@mui/material/Select";
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';


import socket from "../utils/websocket";
import axios from "axios";


Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = createWorldTerrain();
const SentinelTwoImagery = new IonImageryProvider({ assetId: 3954 }); //createWorldImagery() for Bing Imagery
const bingImagery = createWorldImagery(); //createWorldImagery() for Bing Imagery
const simple = new OpenStreetMapImageryProvider({url: 'https://stamen-tiles.a.ssl.fastly.net/toner-background/' });
const url = IonResource.fromAssetId(96188);


const Simulation = () => {
    const viewerRef = useRef<CesiumComponentRef<CesiumViewer>>(null);
    const [czml, setCZML] = useState();
    const [data, setData] = useState<any[]>();
    const [time, setTime] = useState(0);
    const [selectPlot, setSelectPlot] = React.useState('');

    var strokeColor = ["#82ca9d", "#8884d8"]

    useEffect(() => {
      console.log("useEffect() - Cesium Base")

      axios.get("http://localhost:5000/api/simulation").then( res => {
          console.log("replay", res.data);
          setCZML(res.data[0])
          setData(res.data[1])
      }).catch(err => {
          console.log(err);
      })

      // if (viewerRef.current && viewerRef.current.cesiumElement) {
      //   // ref.current.cesiumElement is Cesium's Viewer
      //   // DO SOMETHING
      //   console.log("realtime");
      //   const viewer = viewerRef.current.cesiumElement;
      //   var czmldatasource = new CzmlDataSource();
      //   viewer.dataSources.add(czmldatasource);
      //   socket.on('simulation:all', (msg) => {
      //       console.log("simulation time data received");
      //       czmldatasource.process(msg);
      //   })
      // }
  }, []);

      
    return (
      <Stack height="100vh">
        <Box height="75%">
          <Viewer style={{height: "100%"}} imageryProvider={false} ref={viewerRef} homeButton={false} baseLayerPicker={false} fullscreenButton={false} navigationHelpButton={false} skyAtmosphere={false}>
            <Scene debugShowFramesPerSecond={true}/>
            <Globe terrainProvider={terrainProvider} baseColor={Color.fromCssColorString('#000000')}/>
            {/* <ImageryLayer imageryProvider={simple} alpha={0.2}/> */}
            <ImageryLayer imageryProvider={simple} alpha={0.2} contrast={-1}/>
            <Cesium3DTileset url={url}/>
            <Clock onTick={(clock) => {
              setTime(JulianDate.secondsDifference(clock.currentTime, clock.startTime))
            }}/>
            {czml && <CzmlDataSource data={czml} onLoad={(ds) => {
                console.log(ds);
            }}/>}
          </Viewer>
        </Box>
        <Box height="5%" sx={{ backgroundColor: '#121212' }} display="flex" justifyContent="center" alignItems="center">
          <FormControl size="small" sx={{ width: "200px"}} >
            <InputLabel id="select" sx={{fontSize: 12}}>Plot state variables</InputLabel>
            <Select
              labelId="select"
              id="select-plot"
              value={selectPlot}
              label="Plo state variables"
              onChange={(event) => {
                setSelectPlot(event.target.value);
              }}
              sx={{fontSize: 12}}
            >
              <MenuItem value={0} sx={{fontSize: 12}}>Altitude</MenuItem>
              <MenuItem value={1} sx={{fontSize: 12}}>Heading</MenuItem>
              <MenuItem value={2} sx={{fontSize: 12}}>Thrust</MenuItem>
            </Select>
          </FormControl>
        </Box>
        <Box height="20%" sx={{ backgroundColor: '#121212' }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart>
              {/* <CartesianGrid strokeDasharray="3 3" /> */}
              <XAxis dataKey="time" type="number" unit="s" tick={{fontSize: 12}}/>
              <YAxis dataKey="value" tick={{fontSize: 12}}/>
              <Tooltip />
              <Legend verticalAlign="top" height={25} wrapperStyle={{fontSize: 12}}/>
              {data && data[0].map((d:any) => (
                <Line dataKey="value" data={d.data} name={d.name} key={d.name}  dot={false} type="linear" stroke={strokeColor[d.id]} strokeWidth={1.5}/>
              ))}
              <ReferenceLine x={time} stroke="red" />
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </Stack>
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