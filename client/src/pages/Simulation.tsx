import React, { useState, useRef,} from "react";
import { IonContent, IonPage, IonTitle, IonToolbar, IonRange, IonIcon, IonButtons, IonButton, IonProgressBar, IonLabel, IonItem, IonSelect, IonSelectOption, IonGrid, IonCol, IonRow, IonFooter, IonChip, IonModal, IonToggle, IonList, useIonViewDidEnter, IonHeader, IonSegment, IonSegmentButton, IonLoading } from '@ionic/react';
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, createWorldImagery, OpenStreetMapImageryProvider, Color, JulianDate, CzmlDataSource as cesiumCzmlDataSource} from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef, Scene, ImageryLayer, CzmlDataSource, Clock, Camera } from "resium";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend, ReferenceLine } from "recharts";

import {
    stop, stopOutline,
    playBack, playBackOutline,
    playForward, playForwardOutline,
    folder
} from "ionicons/icons";

import socket from "../utils/websocket"

Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = createWorldTerrain();
const url = IonResource.fromAssetId(96188);
const bingImagery = createWorldImagery();
const simpleImagery = new OpenStreetMapImageryProvider({url: 'https://stamen-tiles.a.ssl.fastly.net/toner-background/' });


const Simulation: React.FC = () => {
    const viewerRef = useRef<CesiumComponentRef<CesiumViewer>>(null);

    // Data - cesium
    const [replayCzml, setReplayCzml] = useState();
    const [navCzml, setNavCzml] = useState();
    const simulationDataSource = new cesiumCzmlDataSource();
    // Data - graph
    const [graphData, setGraphData] = useState([]);
    const [simulationGraphData, setSimulationGraphData] = useState<any>([]);
    // Clock
    const [clockDirection, setClockDirection] = useState(0);
    const [clockMultiplier, setClockMultiplier] = useState(1);
    const [julianDate, setJulianDate] = useState('');
    const [clockTime, setClockTime] = useState(0);
    const [startTime, setStartTime] = useState<any>();
    const [endTime, setEndTime] = useState(100);
    const [changeTime, setChangeTime] = useState(false);
    const [targetTime, setTargetTime] = useState<any>();
    // UI - toolbar
    const [mode, setMode] = useState('');
    const [graph, setGraph] = useState<string>('None');
    const [graphHeader, setGraphHeader] = useState(['None']);
    const [stateliteMode, setStateliteMode] = useState(false);
    const [progressbar, setProgressBar] = useState(0);
    // UI - Pop up modal
    const [replayList, setReplayList] = useState<any>();
    const [replayCategory, setReplayCategory] = useState('historic')
    const [replayFile, setReplayFile] = useState('')
    const [simulationList, setSimulationList] = useState<any>();
    const [isLoading, setIsLoading] = useState(false);
    const [showReplayModal, setShowReplayModal] = useState(false);
    const [showSimulationModal, setShowSimulationModal] = useState(false);


    useIonViewDidEnter(()=> {
        console.log('ionViewDidEnter event fired');
        if (viewerRef.current?.cesiumElement) {
            const viewer = viewerRef.current.cesiumElement;
            console.log(viewer)
            viewer.dataSources.add(simulationDataSource);
        }

        socket.on("connect", () => {
            console.log("SocketIO connected", socket.connected); // True
        });
          
        socket.on("disconnect", () => {
            console.log("SocketIO connected", socket.connected); // False
        });
    
        socket.on("simulationData", (msg) => {
            console.log(msg);
            if (viewerRef.current?.cesiumElement) {
                simulationDataSource.process(msg.czml);
                setSimulationGraphData(simulationGraphData.push(msg.graph))
                setProgressBar(msg.progress);
                if (msg.progress === 1){
                    setProgressBar(0);
                }
            }
        })

        socket.on("simulationGraphHeader", (msg) => {
            console.log(msg);
            setGraphHeader(msg)
        })
    })


    function getReplayDirs(){
        socket.emit("getReplayDir", (res :any) => {
            setReplayList(res)
        });
    }

    function getReplayCZML(dir :string){
        setGraph('None')
        socket.emit("getReplayCZML", replayCategory, dir, (res :any) => {
            setReplayCzml(res);
        });
        getGraphHeader(dir)
    }

    function getGraphHeader(file :string){
        socket.emit("getGraphHeader", mode, replayCategory, file, (res :any) => {
            setGraphHeader(res)
        });
    }

    function getGraphData(graph_type :string){
        socket.emit("getGraphData", mode, replayCategory, replayFile, graph_type, (res :any) => {
            setGraphData(res)
        });
    }

    function getSimulationFile(){
        socket.emit("getSimulationFile", (res :any) => {
            setSimulationList(res)
        });
    }

    function runSimulation(file :string){
        setGraph('None')
        setSimulationGraphData([])
        socket.emit("runSimulation", file);
    }

    function getNav(){
        if (viewerRef.current?.cesiumElement) {
            const viewer = viewerRef.current.cesiumElement;
            var currentMagnitude = viewer.camera.getMagnitude();
            // console.log('current magnitude - ', currentMagnitude);
            // var direction = viewer.camera.direction;
            // console.log("camera direction", direction.x, direction.y, direction.z);
            var rectangle = viewer.camera.computeViewRectangle();
            // console.log("camera rectangle", rectangle!.south/Math.PI*180, rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180);
            if(currentMagnitude < 6700000){
                socket.emit("getNav", rectangle!.south/Math.PI*180, rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180, (res :any) => {
                    setNavCzml(res);
                });
            } else {
                setNavCzml(undefined);
            }
        }
    }

    return (
        <IonPage>
            <IonContent scrollY={false}>
                <Viewer ref={viewerRef} style={{height:"100%"}} useBrowserRecommendedResolution={true} selectionIndicator={false} imageryProvider={false} homeButton={false} baseLayerPicker={false} sceneModePicker={false} fullscreenButton={false} navigationHelpButton={false} timeline={false} geocoder={false} animation={false}>
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
                            setEndTime(JulianDate.secondsDifference(clock.stopTime, clock.startTime));
                            setStartTime(clock.startTime);
                        }} 
                    />
                    <Camera onMoveEnd={() => {getNav()}}/>
                    {replayCzml && mode === 'replay' && <CzmlDataSource data={replayCzml} onLoad={() => {
                        setIsLoading(false);
                    }}/>}
                    {navCzml && <CzmlDataSource data={navCzml}/>}
                </Viewer >
            </IonContent>
            
            <IonLoading isOpen={isLoading} spinner="crescent" message="Loading..."/>

            <IonFooter>
                {progressbar > 0 && <IonProgressBar buffer={progressbar} color='dark'/>}
                <IonToolbar> 
                    <IonGrid fixed style={{"--ion-grid-padding": "0px",  "--ion-grid-column-padding":"0px", "--ion-grid-width-xl":"90%", "--ion-grid-width-lg":"100%", "--ion-grid-width-md":"100%", "--ion-grid-width-sm": "100%", "--ion-grid-width-xs":"100%"}} >
                        <IonRow class="ion-align-items-center ion-justify-content-center">
                            <IonCol size="auto">
                                <IonItem class="ion-no-padding" style={{"width": "150px",  "--inner-padding-end":"0px"}} href="https://github.com/HKUST-OCTAD-LAB/AirTrafficSim" target="_blank">
                                    <IonTitle>AirTrafficSim</IonTitle>
                                </IonItem>
                            </IonCol>
                            <IonCol size="auto">
                                <IonItem class="ion-nowrap ion-no-padding" style={{"width": "200px",  "--inner-padding-end":"0px"}}>
                                    <IonChip outline={mode === 'replay' ? false : true} color="dark" onClick={() => {setMode('replay'); getReplayDirs(); setShowReplayModal(true);}}>
                                        <IonLabel>Replay</IonLabel>
                                    </IonChip>
                                    <IonChip outline={mode === 'simulation' ? false : true} color="dark" onClick={() => {setMode('simulation'); getSimulationFile(); setShowSimulationModal(true);}}>
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
                                                {replayList[replayCategory].map((dir: any) =>
                                                    <IonItem key={dir} button={true} onClick={()=>{setShowReplayModal(false); setIsLoading(true); setReplayFile(dir); getReplayCZML(dir);}}>
                                                        <IonIcon icon={folder} slot="start"/>
                                                        <IonLabel>{dir}</IonLabel>
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
                            {Ion.defaultAccessToken &&
                                <IonCol size="auto">
                                    <IonItem class="ion-no-padding" style={{"width": "150px",  "--inner-padding-end":"0px"}}>
                                        <IonToggle color="medium" onIonChange={(e) => setStateliteMode(e.detail.checked)}/>
                                        <IonLabel>Satellite</IonLabel>
                                    </IonItem>
                                </IonCol>
                            }
                            <IonCol size="auto">
                                <IonItem style={{"width": "120px"}}>
                                    <IonLabel position="stacked">Show graph</IonLabel>
                                    <IonSelect color='dark' interface="alert" placeholder="type" value={graph} onIonChange={e => {getGraphData(e.detail.value); setGraph(e.detail.value);}}>
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
                                <IonItem  style={{"width": "100px", "--inner-padding-end":"0px"}}>
                                    <IonLabel style={{"whiteSpace": "pre-line"}} class="ion-text-center">{julianDate}</IonLabel>
                                </IonItem>
                            </IonCol>
                            <IonCol >
                                <IonItem >
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
                {graph !== 'None' &&
                    <IonItem>
                        <ResponsiveContainer height={200}>
                            <LineChart>
                            <XAxis dataKey="time" type="number" unit="s" tick={{fontSize: 12}}/>
                            <YAxis dataKey="value" tick={{fontSize: 12}} domain={['auto', 'auto']}/>
                            <Tooltip />
                            <Legend verticalAlign="top" height={25} wrapperStyle={{fontSize: 12}}/>
                            {graphData && graphData.map((d:any) => (
                                <Line dataKey="value" data={d.data} name={d.name} key={d.name} dot={false} type="linear" stroke={d.color} strokeWidth={1.5}/>
                            ))}
                            <ReferenceLine x={Math.trunc(clockTime)} stroke="red" />
                            </LineChart>
                        </ResponsiveContainer>
                    </IonItem>
                }
            </IonFooter>
        </IonPage>
    );
};

export default Simulation;
