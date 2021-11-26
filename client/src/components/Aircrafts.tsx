import React, {useEffect, useState } from "react";
import { CzmlDataSource } from "resium";
import socket from '../utils/websocket';


const Aircrafts = () => {
    const [dataSource, setDataSource] = useState();

    useEffect(() => {
        console.log("useEffect - Aircrafts")

        socket.on('realtime:all', (msg) => {
            console.log(msg);
            setDataSource(msg);
        })
    }, [])

    return (
        <CzmlDataSource data={dataSource} onLoad={(ds) => {
            console.log(ds);
        }}/>
    );
}

export default Aircrafts;