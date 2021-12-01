import { CzmlDataSource, Viewer } from "cesium";
import socket from '../utils/websocket';

export const realtime = (viewer:Viewer) => {
    console.log("realtime");
    var czmldatasource = new CzmlDataSource();
    viewer.dataSources.add(czmldatasource);
    socket.on('realtime:all', (msg) => {
        // console.log("real time data received");
        czmldatasource.process(msg);
    })
}