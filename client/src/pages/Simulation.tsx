import React, { useState, useRef,} from "react";
import { IonContent, IonPage, IonTitle, IonToolbar, IonRange, IonIcon, IonButtons, IonButton, IonProgressBar, IonLabel, IonItem, IonSelect, IonSelectOption, IonGrid, IonCol, IonRow, IonFooter, IonChip, IonModal, IonToggle, IonList, useIonViewDidEnter, IonHeader, IonSegment, IonSegmentButton, IonLoading, IonToast } from '@ionic/react';
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, createWorldImagery, OpenStreetMapImageryProvider, Color, JulianDate, CzmlDataSource as cesiumCzmlDataSource, HeadingPitchRange, WebMapServiceImageryProvider, MapboxStyleImageryProvider, Cesium3DTileStyle} from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef, Scene, ImageryLayer, Clock, Camera } from "resium";
import Plotly from "plotly.js-gl2d-dist-min";
import createPlotlyComponent from "react-plotly.js/factory";

import {
    stop, stopOutline,
    playBack, playBackOutline,
    playForward, playForwardOutline,
    folder, settings
} from "ionicons/icons";

import socket from "../utils/websocket"

const Plot = createPlotlyComponent(Plotly);

Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = createWorldTerrain();
const osmBuilding = IonResource.fromAssetId(96188);
const osmBuildingstyle = new Cesium3DTileStyle({
    color : 'color("grey")'z
});
const bingImagery = createWorldImagery();
const simpleImagery = new OpenStreetMapImageryProvider({url: 'https://stamen-tiles.a.ssl.fastly.net/toner-background/' });
const mapboxImagery = new MapboxStyleImageryProvider({
    styleId: 'dark-v10',
    accessToken: process.env.REACT_APP_MAPBOX_ACCESS_TOKEN!
});

const replayDataSource = new cesiumCzmlDataSource();
const simulationDataSource = new cesiumCzmlDataSource();
const navDataSource = new cesiumCzmlDataSource();
const era5WindDataSource = new cesiumCzmlDataSource();
const era5RainDataSource = new cesiumCzmlDataSource();
const radarImageDataSource = new cesiumCzmlDataSource();

const defaultZoom = new HeadingPitchRange(0,-90,500000);
const nexrad = new WebMapServiceImageryProvider({
    url:
      "https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi?",
    layers: "nexrad-n0r",
    credit: "Radar data courtesy Iowa Environmental Mesonet",
    parameters: {
      transparent: "true",
      format: "image/png",
    },
  })


const Simulation: React.FC = () => {
    const viewerRef = useRef<CesiumComponentRef<CesiumViewer>>(null);

    // Clock
    const [clockDirection, setClockDirection] = useState(0);
    const [clockMultiplier, setClockMultiplier] = useState(1);
    const [startTime, setStartTime] = useState<any>();
    const [endTime, setEndTime] = useState(100);
    const [julianDate, setJulianDate] = useState('');
    const [clockTime, setClockTime] = useState(0);
    const [changeTime, setChangeTime] = useState(false);
    const [targetTime, setTargetTime] = useState<any>();
    // UI - toolbar
    const [mode, setMode] = useState('');
    const [connected, setConnected] = useState(false);    
    const [stateliteMode, setStateliteMode] = useState(false);
    const [era5Wind, setEra5Wind] = useState(false);
    const [era5Rain, setEra5Rain] = useState(false);
    const [radar, setRadar] = useState(false);
    const [progressBar, setProgressBar] = useState(0);
    const [graphType, setGraphType] = useState<string>('None');
    const [graphHeader, setGraphHeader] = useState(['None']);
    const [graphData, setGraphData] = useState([]);
    // UI - Pop up modal
    const [replayList, setReplayList] = useState<any>();
    const [replayCategory, setReplayCategory] = useState('historic')
    const [replayFile, setReplayFile] = useState('')
    const [simulationList, setSimulationList] = useState<any>();
    const [simulationFile, setSimulationFile] = useState('')
    const [isLoading, setIsLoading] = useState(false);
    const [showReplayModal, setShowReplayModal] = useState(false);
    const [showSimulationModal, setShowSimulationModal] = useState(false);
    const [showSettingModal, setShowSettingModal] = useState(false);
    const [showNavigationData, setShowNavigationData] = useState(false);


    useIonViewDidEnter(()=> {
        if (viewerRef.current?.cesiumElement) {
            const viewer = viewerRef.current.cesiumElement;
            viewer.dataSources.add(replayDataSource);
            viewer.dataSources.add(simulationDataSource);
            viewer.dataSources.add(navDataSource);
            viewer.dataSources.add(era5WindDataSource);
            viewer.dataSources.add(era5RainDataSource);
            viewer.dataSources.add(radarImageDataSource);
            setStartTime(viewer.clock.startTime)
        }

        setConnected(socket.connected);

        socket.on("connect", () => {
            setConnected(socket.connected)
        });
          
        socket.on("disconnect", () => {
            setConnected(socket.connected)
        });
    
        socket.on("simulationData", (msg) => {
            simulationDataSource.process(msg.czml).then(ds => {
                if (viewerRef.current?.cesiumElement) {
                    setEndTime(JulianDate.secondsDifference(ds.clock.stopTime, ds.clock.startTime));
                    setStartTime(ds.clock.startTime);
                }
            });
            if (msg.packet_id === 0 && viewerRef.current?.cesiumElement) {
                const viewer = viewerRef.current.cesiumElement;
                viewer.clockTrackedDataSource = simulationDataSource;
                viewer.zoomTo(simulationDataSource, defaultZoom);
            }
            setIsLoading(false);
            setGraphData(msg.graph);
            if (msg.progress === 1){
                setProgressBar(0);
            } else {
                setProgressBar(msg.progress);
            }
        })

        socket.on("simulationEnvironment", (msg) => {
            setGraphHeader(msg.header);
            setSimulationFile(msg.file);
        })
    })

    function getReplayDirs(){
        socket.emit("getReplayDir", (res :any) => {
            setReplayList(res)
        });
    }

    function getReplayCZML(dir :string){
        setGraphType('None')
        socket.emit("getReplayCZML", replayCategory, dir, (res :any) => {
            replayDataSource.load(res).then(ds => {
                if (viewerRef.current?.cesiumElement) {
                    setEndTime(JulianDate.secondsDifference(ds.clock.stopTime, ds.clock.startTime));
                    setStartTime(ds.clock.startTime);
                    const viewer = viewerRef.current.cesiumElement;
                    viewer.clockTrackedDataSource = ds
                    viewer.zoomTo(ds, defaultZoom)
                }
            });
            setIsLoading(false);
        });
        getGraphHeader(dir)
    }

    function getGraphHeader(file :string){
        socket.emit("getGraphHeader", mode, replayCategory, file, (res :any) => {
            setGraphHeader(res)
        });
    }

    function getGraphData(graph_type :string){
        if (progressBar === 0){
            socket.emit("getGraphData", mode, replayCategory, replayFile, simulationFile, graph_type, (res :any) => {
                setGraphData(res)
            });
        }
    }

    function getSimulationFile(){
        socket.emit("getSimulationFile", (res :any) => {
            setSimulationList(res)
        });
    }

    function runSimulation(file :string){
        setGraphType('None')
        setIsLoading(true)
        socket.emit("runSimulation", file);
    }

    function clearData(){
        replayDataSource.entities.removeAll();
        simulationDataSource.entities.removeAll();
    }

    function getNav(selected :boolean, value: boolean){
        let get = false
        if (selected){
            get = value
        } else {
            get = showNavigationData
        }
        if (get && viewerRef.current?.cesiumElement) {
            const viewer = viewerRef.current.cesiumElement;
            var currentMagnitude = viewer.camera.getMagnitude();
            // console.log('current magnitude - ', currentMagnitude);
            // var direction = viewer.camera.direction;
            // console.log("camera direction", direction.x, direction.y, direction.z);
            var rectangle = viewer.camera.computeViewRectangle();
            // console.log("camera rectangle", rectangle!.south/Math.PI*180, rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180);
            if(currentMagnitude < 6800000){
                socket.emit("getNav", rectangle!.south/Math.PI*180, rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180, (res :any) => {
                    navDataSource.load(res);
                });
            } else {
                navDataSource.entities.removeAll();
            }
        } else {
            navDataSource.entities.removeAll();
        }
    }

    function getEra5Wind(selected :boolean, value: boolean){
        let get = false
        if (selected){
            get = value
        } else {
            get = era5Wind
        }
        if (get && viewerRef.current?.cesiumElement){
            const viewer = viewerRef.current.cesiumElement;
            var currentMagnitude = viewer.camera.getMagnitude();
            // console.log('current magnitude - ', currentMagnitude);
            // var direction = viewer.camera.direction;
            // console.log("camera direction", direction.x, direction.y, direction.z);
            var rectangle = viewer.camera.computeViewRectangle();
            if(currentMagnitude < 10000000){
                socket.emit("getEra5Wind", rectangle!.south/Math.PI*180, rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180, mode==='replay'?replayFile:simulationFile, (res :any) => {
                    era5WindDataSource.process(res);
                });
            } else {
                era5WindDataSource.entities.removeAll();
            }
        } else {
            era5WindDataSource.entities.removeAll();
        }
    }

    function getEra5Rain(selected :boolean, value: boolean){
        let get = false
        if (selected){
            get = value
        } else {
            get = era5Rain
        }
        if (get && viewerRef.current?.cesiumElement){
            const viewer = viewerRef.current.cesiumElement;
            var currentMagnitude = viewer.camera.getMagnitude();
            // console.log('current magnitude - ', currentMagnitude);
            // var direction = viewer.camera.direction;
            // console.log("camera direction", direction.x, direction.y, direction.z);
            var rectangle = viewer.camera.computeViewRectangle();
            if(currentMagnitude < 40000000){
                socket.emit("getEra5Rain", rectangle!.south/Math.PI*180, rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180, mode==='replay'?replayFile:simulationFile, (res :any) => {
                    era5RainDataSource.process(res);
                });
            } else {
                era5RainDataSource.entities.removeAll();
            }
        } else {
            era5RainDataSource.entities.removeAll();
        }
    }

    function getRadarImg(selected :boolean, value: boolean){
        let get = false
        if (selected){
            get = value
        } else {
            get = radar
        }
        if (get && viewerRef.current?.cesiumElement){
            const viewer = viewerRef.current.cesiumElement;
            var currentMagnitude = viewer.camera.getMagnitude();
            // console.log('current magnitude - ', currentMagnitude);
            // var direction = viewer.camera.direction;
            // console.log("camera direction", direction.x, direction.y, direction.z);
            var rectangle = viewer.camera.computeViewRectangle();
            socket.emit("getRadarImage", rectangle!.south/Math.PI*180, rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180, mode==='replay'?replayFile:simulationFile, (res :any) => {
                console.log(res);
                radarImageDataSource.process(res);
            });
        } else {
            radarImageDataSource.entities.removeAll();
        }
    }

    return (
        <IonPage>
            <IonContent scrollY={false}>
                <Viewer ref={viewerRef} style={{height:"100%"}} animation={false} timeline={false} selectionIndicator={false} imageryProvider={false} homeButton={false} baseLayerPicker={false} sceneModePicker={false} fullscreenButton={false} navigationHelpButton={false} geocoder={false} >
                    <Scene debugShowFramesPerSecond={true}/>
                    <Globe baseColor={Color.fromCssColorString('#000000')} terrainProvider={Ion.defaultAccessToken ? terrainProvider : undefined} showGroundAtmosphere={false}/>
                    <ImageryLayer imageryProvider={bingImagery}  show={stateliteMode}/>
                    {process.env.REACT_APP_MAPBOX_ACCESS_TOKEN ? <ImageryLayer imageryProvider={mapboxImagery} show={!stateliteMode}/> : <ImageryLayer imageryProvider={simpleImagery} alpha={0.3} contrast={-1} show={!stateliteMode}/>}
                    {/* <ImageryLayer imageryProvider={nexrad}/> */}
                    {Ion.defaultAccessToken && <Cesium3DTileset url={osmBuilding} style={osmBuildingstyle}/>}
                    <Clock 
                        shouldAnimate={clockDirection !== 0 ? true : false} 
                        multiplier={clockMultiplier * clockDirection}
                        currentTime={targetTime}
                        onTick={(clock) => {
                            setClockTime(JulianDate.secondsDifference(clock.currentTime, clock.startTime));
                            setJulianDate(JulianDate.toIso8601(clock.currentTime, 0).replace("T", "\n"));
                        }} 
                    />
                    <Camera onMoveEnd={() => {getNav(false, false); getEra5Wind(false, false); getEra5Rain(false, false);}}/>
                </Viewer>
            </IonContent>
            
            <IonLoading isOpen={isLoading} spinner="crescent" message="Loading..."/>
            <IonToast isOpen={!connected} message="Connecting. Please refresh." position='top' color='light'/>
            <IonFooter>
            {progressBar > 0 && <IonProgressBar value={progressBar} color='dark'/>}
                <IonToolbar> 
                    <IonGrid fixed style={{"--ion-grid-padding": "0px",  "--ion-grid-column-padding":"0px", "--ion-grid-width-xl":"90%", "--ion-grid-width-lg":"100%", "--ion-grid-width-md":"100%", "--ion-grid-width-sm": "100%", "--ion-grid-width-xs":"100%"}} >
                        <IonRow class="ion-align-items-center ion-justify-content-center">
                            <IonCol size="auto">
                                <IonItem class="ion-no-padding" lines="none" style={{"width": "150px", "height" : "100%", "--inner-padding-end":"0px", "--background": "transparent"}} href="https://github.com/HKUST-OCTAD-LAB/AirTrafficSim" target="_blank">
                                    <IonTitle>AirTrafficSim</IonTitle>
                                </IonItem>
                            </IonCol>
                            <IonCol size="auto">
                                <IonItem class="ion-nowrap ion-no-padding" lines="none" style={{"width": "200px",  "--inner-padding-end":"0px", "--background": "transparent"}}>
                                    <IonChip outline={mode === 'replay' ? false : true} color="dark" onClick={() => {setMode('replay'); getReplayDirs(); setShowReplayModal(true); clearData();}}>
                                        <IonLabel>Replay</IonLabel>
                                    </IonChip>
                                    <IonChip outline={mode === 'simulation' ? false : true} color="dark" onClick={() => {setMode('simulation'); getSimulationFile(); setShowSimulationModal(true); clearData();}}>
                                        <IonLabel>Simulation</IonLabel>
                                    </IonChip>
                                </IonItem>
                                
                                <IonModal isOpen={showReplayModal} onDidDismiss={()=>setShowReplayModal(false)}>
                                    <IonHeader translucent>
                                        <IonToolbar>
                                            <IonTitle size="large">Select replay files</IonTitle>
                                        </IonToolbar>
                                        <IonToolbar>
                                        <IonSegment color="dark" value={replayCategory} onIonChange={e => setReplayCategory(e.detail.value!)}>
                                                <IonSegmentButton value="historic">
                                                    <IonLabel>Historic</IonLabel>
                                                </IonSegmentButton>
                                                <IonSegmentButton value="simulation">
                                                    <IonLabel>Simulation</IonLabel>
                                                </IonSegmentButton>
                                            </IonSegment>
                                        </IonToolbar>
                                    </IonHeader>
                                    <IonContent fullscreen>
                                        {replayList &&
                                            <IonList>
                                                {replayList[replayCategory].map((file: any) =>
                                                    <IonItem key={file} button={replayCategory === "historic"? true: false} 
                                                        onClick={()=>{
                                                            if (replayCategory === "historic"){
                                                                setShowReplayModal(false); setIsLoading(true); setReplayFile(file); getReplayCZML(file);
                                                            }
                                                    }}>
                                                        <IonIcon icon={folder} slot="start"/>
                                                        <IonLabel>{file}</IonLabel>
                                                        {replayCategory === "simulation" &&
                                                            <IonSelect color='dark' interface="alert"
                                                                onIonChange={e => {setShowReplayModal(false); setIsLoading(true); setReplayFile(file+"/"+e.detail.value); getReplayCZML(file+"/"+e.detail.value);}}>
                                                                    {replayList["simulation_files"][file].map((f :string) => 
                                                                        <IonSelectOption key={f} value={f}>{f}</IonSelectOption>
                                                                    )}
                                                            </IonSelect>
                                                        }
                                                    </IonItem>
                                                )}
                                            </IonList>
                                        }
                                    </IonContent>
                                </IonModal>

                                <IonModal isOpen={showSimulationModal} onDidDismiss={()=>setShowSimulationModal(false)}>
                                    <IonHeader translucent>
                                        <IonToolbar>
                                            <IonTitle size="large">Select simulation environment</IonTitle>
                                        </IonToolbar>
                                    </IonHeader>
                                    <IonContent fullscreen>
                                        {simulationList &&
                                            <IonList>
                                                {simulationList.map((file: string) =>
                                                    <IonItem key={file} button={true} onClick={()=>{setShowSimulationModal(false); runSimulation(file);}}>
                                                        <IonIcon icon={folder} slot="start"/>
                                                        <IonLabel>{file}</IonLabel>
                                                    </IonItem>
                                                )}
                                            </IonList>
                                        }
                                    </IonContent>
                                </IonModal>
                            </IonCol>
                            <IonCol size="auto">
                                <IonItem class="ion-no-padding" lines="none" style={{"width": "100px",  "--inner-padding-end":"0px", "--background": "transparent"}} button={true} onClick={() => setShowSettingModal(true)}>
                                    <IonIcon icon={settings}/>
                                    <IonLabel class="ion-text-center">Settings</IonLabel>
                                </IonItem>
                                <IonModal isOpen={showSettingModal} onDidDismiss={()=>setShowSettingModal(false)} style={{"--width":"300px", "--height": "300px"}}>
                                    <IonContent>
                                        <IonHeader translucent>
                                            <IonToolbar>
                                                <IonTitle size="large">Settings</IonTitle>
                                            </IonToolbar>
                                        </IonHeader>
                                        <IonItem>
                                            <IonToggle color="medium" checked={stateliteMode} onIonChange={(e) => setStateliteMode(e.detail.checked)}/>
                                            <IonLabel>Statelite imagery</IonLabel>
                                        </IonItem>
                                        <IonItem>
                                            <IonToggle color="medium" checked={showNavigationData} onIonChange={(e) => {setShowNavigationData(e.detail.checked); getNav(true, e.detail.checked);}}/>
                                            <IonLabel>Navigation Data</IonLabel>
                                        </IonItem>
                                        <IonItem>
                                            <IonToggle color="medium" disabled={mode === ''} checked={era5Wind} onIonChange={(e) => {setEra5Wind(e.detail.checked); getEra5Wind(true, e.detail.checked)}}/>
                                            <IonLabel>ERA5 Wind</IonLabel>
                                        </IonItem>
                                        <IonItem>
                                            <IonToggle color="medium" disabled={mode === ''} checked={era5Rain} onIonChange={(e) => {setEra5Rain(e.detail.checked); getEra5Rain(true, e.detail.checked)}}/>
                                            <IonLabel>ERA5 Rain</IonLabel>
                                        </IonItem>
                                        <IonItem>
                                            <IonToggle color="medium" disabled={mode === ''} checked={radar} onIonChange={(e) => {setRadar(e.detail.checked); getRadarImg(true, e.detail.checked)}}/>
                                            <IonLabel>Radar Image</IonLabel>
                                        </IonItem>
                                    </IonContent>
                                </IonModal>
                            </IonCol>
                            <IonCol size="auto">
                                <IonItem lines="none" style={{"width": "150px", "--background": "transparent"}}>
                                    <IonLabel position="stacked">Show graph</IonLabel>
                                    <IonSelect color='dark' interface="alert" placeholder="type" value={graphType}
                                    onIonChange={e => {getGraphData(e.detail.value); setGraphType(e.detail.value); if (mode==='simulation'){socket.emit('setSimulationGraphType', e.detail.value)}}}>
                                        {graphHeader.map((header :string) => 
                                            <IonSelectOption key={header} value={header}>{header}</IonSelectOption>
                                        )}
                                    </IonSelect>
                                </IonItem>
                            </IonCol>
                            

                            <IonCol size="auto">
                                <IonButtons style={{"width": "220px"}}>
                                    <IonButton onClick={() => setClockDirection(-1)}>
                                        {clockDirection < 0 ? <IonIcon icon={playBack} slot="icon-only"/> : <IonIcon icon={playBackOutline} slot="icon-only"/>}
                                    </IonButton>
                                    <IonButton onClick={() => setClockDirection(0)}>
                                        {clockDirection === 0 ? <IonIcon icon={stop} slot="icon-only"/> : <IonIcon icon={stopOutline} slot="icon-only"/>}
                                    </IonButton>
                                    
                                    <IonButton onClick={() => setClockDirection(1)}> 
                                        {clockDirection > 0 ? <IonIcon icon={playForward} slot="icon-only"/> : <IonIcon icon={playForwardOutline} slot="icon-only"/>}
                                    </IonButton>
                                    <IonSelect color='dark' interface="popover" value={clockMultiplier} onIonChange={e => setClockMultiplier(e.detail.value)}>
                                        <IonSelectOption value={1}>  1X</IonSelectOption>
                                        <IonSelectOption value={2}>  2X</IonSelectOption>
                                        <IonSelectOption value={5}>  5X</IonSelectOption>
                                        <IonSelectOption value={10}> 10X</IonSelectOption>
                                        <IonSelectOption value={20}> 20X</IonSelectOption>
                                        <IonSelectOption value={50}> 50X</IonSelectOption>
                                        <IonSelectOption value={100}>100X</IonSelectOption>
                                    </IonSelect>
                                </IonButtons>
                            </IonCol>
                            <IonCol size="auto">
                                <IonItem lines="none" style={{"width": "100px", "--inner-padding-end":"0px", "--background": "transparent"}}>
                                    <IonLabel style={{"whiteSpace": "pre-line"}} class="ion-text-center">{julianDate}</IonLabel>
                                </IonItem>
                            </IonCol>
                            <IonCol >
                                <IonItem lines="none" style={{"--background": "transparent"}}>
                                    <IonRange min={0} max={endTime} value={clockTime} color='dark'
                                        onIonChange={(e) => {if(changeTime){
                                                                const target:any = e.detail.value;
                                                                setClockTime(target)
                                                                setTargetTime(JulianDate.addSeconds(startTime, target, JulianDate.clone(startTime)));
                                                            }}}
                                        onIonFocus={() => {setClockDirection(0); setChangeTime(true);}}
                                        onIonBlur={()=>{setChangeTime(false)}}
                                    >
                                        <IonLabel slot="start">{Math.trunc(clockTime) + "s"}</IonLabel>
                                    </IonRange>
                                </IonItem>
                            </IonCol>
                        </IonRow>
                    </IonGrid>                   
                </IonToolbar>  
                {graphType !== 'None' &&
                    <IonItem lines="none" >
                      <div style={{height:"200px", width:"100%"}}>
                      <Plot
                        data={graphData}
                        layout={{
                            autosize: true, paper_bgcolor: "transparent", plot_bgcolor: "transparent", 
                            margin:{b:35, t:5, l:30, r: 30,},
                            legend: {orientation: "v", x:1, y:0.5},
                            yaxis: {showgrid: false, showline:true, zeroline: false},
                            xaxis: {showgrid: false, showline:true, title:{text:"time (s)"}},
                            shapes:[{
                                type: "line", 
                                yref: "paper", y0:0, y1: 1,
                                xref: "x", x0: Math.trunc(clockTime), x1: Math.trunc(clockTime),
                                line: {color: "red", width:1}
                            }],
                            hovermode:"x",
                            modebar:{bgcolor:"transparent"},
                            dragmode: "pan"
                        }}
                        config={{displaylogo: false, scrollZoom: true, showTips:false}}
                        style={{width:"100%", height:"100%"}}
                        useResizeHandler={true}
                      />
                      </div>
                      
                    </IonItem>
                }
            </IonFooter>
        </IonPage>
    );
};

export default Simulation;
