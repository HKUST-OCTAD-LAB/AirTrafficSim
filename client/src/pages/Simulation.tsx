import React, { useState, useRef,} from "react";
import { IonContent, IonPage, IonTitle, IonToolbar, IonRange, IonIcon, IonButtons, IonButton, IonProgressBar, IonLabel, IonItem, IonSelect, IonSelectOption, IonGrid, IonCol, IonRow, IonFooter, IonChip, IonModal, IonToggle, IonList, useIonViewDidEnter, IonHeader, IonSegment, IonSegmentButton, IonLoading, IonToast } from '@ionic/react';
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, createWorldImagery, OpenStreetMapImageryProvider, Color, JulianDate, CzmlDataSource as cesiumCzmlDataSource, HeadingPitchRange} from "cesium";
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
const url = IonResource.fromAssetId(96188);
const bingImagery = createWorldImagery();
const simpleImagery = new OpenStreetMapImageryProvider({url: 'https://stamen-tiles.a.ssl.fastly.net/toner-background/' });
const replayDataSource = new cesiumCzmlDataSource();
const simulationDataSource = new cesiumCzmlDataSource();
const navDataSource = new cesiumCzmlDataSource();
const defaultZoom = new HeadingPitchRange(0,-90,500000)


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
        let getNav = false
        if (selected){
            getNav = value
        } else {
            getNav = showNavigationData
        }
        if (getNav && viewerRef.current?.cesiumElement) {
            const viewer = viewerRef.current.cesiumElement;
            var currentMagnitude = viewer.camera.getMagnitude();
            // console.log('current magnitude - ', currentMagnitude);
            // var direction = viewer.camera.direction;
            // console.log("camera direction", direction.x, direction.y, direction.z);
            var rectangle = viewer.camera.computeViewRectangle();
            // console.log("camera rectangle", rectangle!.south/Math.PI*180, rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180);
            if(currentMagnitude < 6800000){
                socket.emit("getNav", rectangle!.south/Math.PI*180, rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180, (res :any) => {
                    navDataSource.load(res)
                });
            } else {
                navDataSource.entities.removeAll();
            }
        } else {
            navDataSource.entities.removeAll();
        }
    }

    return (
        <IonPage>
            <IonContent scrollY={false}>
                <Viewer ref={viewerRef} style={{height:"100%"}} animation={false} timeline={false} selectionIndicator={false} imageryProvider={false} homeButton={false} baseLayerPicker={false} sceneModePicker={false} fullscreenButton={false} navigationHelpButton={false} geocoder={false} >
                    <Scene debugShowFramesPerSecond={true}/>
                    {Ion.defaultAccessToken? <Globe baseColor={Color.fromCssColorString('#000000')} terrainProvider={terrainProvider}/> : <Globe baseColor={Color.fromCssColorString('#000000')} />}
                    {stateliteMode ? <ImageryLayer imageryProvider={bingImagery}/> : <ImageryLayer imageryProvider={simpleImagery} alpha={0.2} contrast={-1}/>}
                    {Ion.defaultAccessToken && <Cesium3DTileset url={url}/>}
                    <Clock 
                        shouldAnimate={clockDirection !== 0 ? true : false} 
                        multiplier={clockMultiplier * clockDirection}
                        currentTime={targetTime}
                        onTick={(clock) => {
                            setClockTime(JulianDate.secondsDifference(clock.currentTime, clock.startTime));
                            setJulianDate(JulianDate.toIso8601(clock.currentTime, 0).replace("T", "\n"));
                        }} 
                    />
                    <Camera onMoveEnd={() => {getNav(false, false)}}/>
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
                                                    <IonItem key={file} button={true} onClick={()=>{setShowReplayModal(false); setIsLoading(true); setReplayFile(file); getReplayCZML(file);}}>
                                                        <IonIcon icon={folder} slot="start"/>
                                                        <IonLabel>{file}</IonLabel>
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
