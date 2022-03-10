import React, { useState, useRef, useEffect} from "react";
import { IonContent, IonPage, IonTitle, IonToolbar, IonRange, IonIcon, IonButtons, IonButton, IonProgressBar, IonLabel, IonItem, IonSelect, IonSelectOption, IonGrid, IonCol, IonRow, IonFooter, IonChip, IonModal, IonToggle, IonList, useIonViewDidEnter, IonHeader, IonSegment, IonSegmentButton, IonLoading } from '@ionic/react';
import { Ion, IonResource, createWorldTerrain, Viewer as CesiumViewer, createWorldImagery, OpenStreetMapImageryProvider, Color, JulianDate} from "cesium";
import { Viewer, Globe, Cesium3DTileset, CesiumComponentRef, Scene, ImageryLayer, CzmlDataSource, Clock } from "resium";
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend, ReferenceLine, CartesianGrid } from "recharts";

import {
    stop, stopOutline,
    playBack, playBackOutline,
    playForward, playForwardOutline,
    folder
} from "ionicons/icons";

import socket from "../utils/websocket";
import axios from "axios";
import { io } from "socket.io-client";

// const socket = io("http://localhost:6000");
// const socket = io();


axios.defaults.baseURL = 'http://127.0.0.1:8000/api/';


Ion.defaultAccessToken = process.env.REACT_APP_CESIUMION_ACCESS_TOKEN!;
const terrainProvider = createWorldTerrain();
const url = IonResource.fromAssetId(96188);
const bingImagery = createWorldImagery();
const simpleImagery = new OpenStreetMapImageryProvider({url: 'https://stamen-tiles.a.ssl.fastly.net/toner-background/' });


const Simulation: React.FC = () => {
    const viewerRef = useRef<CesiumComponentRef<CesiumViewer>>(null);

    // Data - cesium
    const [replayCzml, setReplayCzml] = useState();
    // Data - graph

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
    const [stateliteMode, setStateliteMode] = useState(false);
    // UI - Pop up modal
    const [replayList, setReplayList] = useState<any>();
    const [replayCategory, setReplayCategory] = useState('historic')
    const [replayFile, setReplayFile] = useState('')
    const [isLoading, setIsLoading] = useState(false);
    const [showReplayModal, setShowReplayModal] = useState(false);
    const [showSimulationModal, setShowSimulationModal] = useState(false);


    useIonViewDidEnter(()=> {
        console.log('ionViewDidEnter event fired');
        if (viewerRef.current?.cesiumElement) {
            // ref.current.cesiumElement is Cesium's Viewer
            // DO SOMETHING
            const viewer = viewerRef.current.cesiumElement;
            console.log(viewer)
            // var czmldatasource = new CzmlDataSource();
            // viewer.dataSources.add(czmldatasource);
            // socket.on('realtime:all', (msg) => {
            //     console.log("real time data received");
            //     czmldatasource.process(msg);
            // })
        }
    })
    

    const onCameraChange = (viewer:CesiumViewer) => {
        console.log(viewer);
        var currentMagnitude = viewer.camera.getMagnitude();
        console.log('current magnitude - ', currentMagnitude);
        var direction = viewer.camera.direction;
        console.log("camera direction", direction.x, direction.y, direction.z);
        var rectangle = viewer.camera.computeViewRectangle();
        console.log("camera rectangle", rectangle!.west/Math.PI*180, rectangle!.north/Math.PI*180, rectangle!.east/Math.PI*180, rectangle!.south/Math.PI*180);
    }

    function getReplayDirs(){
        axios.get("replay/").then( res => {
            console.log("replay", res.data);
            setReplayList(res.data)
        }).catch(err => {
            console.log(err);
        })
    }

    function getReplayCZML(category:string, file:string){
        axios.get("replay/"+category+"/"+file).then( res => {
            console.log("replay", res.data);
            setReplayCzml(res.data)
        }).catch(err => {
            console.log(err);
        })
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
                    {replayCzml && <CzmlDataSource data={replayCzml} onLoad={(ds) => {
                        setIsLoading(false);
                        console.log(ds);
                    }}/>}
                </Viewer >
            </IonContent>
            
            <IonLoading isOpen={isLoading} message="Loading..."/>

            <IonFooter>
                <IonProgressBar value={0.25} buffer={0.5} color='dark'/>   
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
                                    <IonChip outline={mode === 'simulation' ? false : true} color="dark" onClick={() => {setMode('simulation'); setShowSimulationModal(true);}}>
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
                                                    <IonItem key={dir} button={true} onClick={()=>{setShowReplayModal(false); setIsLoading(true); getReplayCZML(replayCategory, dir);}}>
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
                                    <IonSelect color='dark' interface="popover" placeholder="Type" onIonChange={e => setGraph(e.detail.value)}>
                                        <IonSelectOption value="None">None</IonSelectOption>
                                        <IonSelectOption value="blonde">Blonde</IonSelectOption>
                                        <IonSelectOption value="black">Black</IonSelectOption>
                                        <IonSelectOption value="red">Red</IonSelectOption>
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
                    <IonItem style={{"height": "200px"}}>
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart>
                            {/* <CartesianGrid strokeDasharray="3 3" /> */}
                            <XAxis dataKey="time" type="number" unit="s" tick={{fontSize: 12}}/>
                            <YAxis dataKey="value" tick={{fontSize: 12}}/>
                            <Tooltip />
                            <Legend verticalAlign="top" height={25} wrapperStyle={{fontSize: 12}}/>
                            {/* {data && data[graph].map((d:any) => (
                                <Line dataKey="value" data={d.data} name={d.name} key={d.name}  dot={false} type="linear" stroke={strokeColor[d.id]} strokeWidth={1.5}/>
                            ))} */}
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
