import React, {useEffect, useRef } from "react";
import { CzmlDataSource } from "resium";
import { io } from "socket.io-client";
// import socket from '../utils/websocket';

const socket = io("ws://localhost:5000");

const Aircrafts = () => {
    
    console.log(socket);

    socket.on('abc', (msg) => {
        console.log(msg);
    })

    return (
        <CzmlDataSource/>
    );
}

export default Aircrafts;