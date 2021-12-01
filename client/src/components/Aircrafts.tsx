import React, {useEffect, useState } from "react";
import { CzmlDataSource } from "resium";
import axios from "axios";


const Aircrafts = () => {
    const [dataSource, setDataSource] = useState();

    useEffect(() => {
        console.log("useEffect - Aircrafts")

        axios.get("http://localhost:5000/replay").then( res => {
            console.log(res.data);
            setDataSource(res.data);
        }).catch(err => {
            console.log(err);
        })
    }, [])

    return (
        <CzmlDataSource data={dataSource} onLoad={(ds) => {
            console.log(ds);
        }}/>
    );
}

export default Aircrafts;