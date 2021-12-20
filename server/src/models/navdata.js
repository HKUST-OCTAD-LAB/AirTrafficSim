const sqlite3 = require('sqlite3');
let db = new sqlite3.Database('../nav/little_navmap_navigraph.sqlite', sqlite3.OPEN_READWRITE, (err) => {
    if (err){
        console.log("Getting error " + err);
    }
    console.log("succesefuly open db");
});

module.exports = {
    navdata: navdata = (callback) => {
        console.log("function - navdata");
        
        // db.get(`SELECt * FROM airport WHERE ident='VHHH'`, [], (err, airport) => {
        //     console.log(airport);
        //     db.all(`SELECT * FROM waypoint WHERE airport_id=${airport.airport_id};`, [], (err, waypoints) => {
        //         if (err){
        //             console.log(err);
        //         }
        //         console.log(waypoints)
        //     }); 
        // })

        const document = [
            {
            "id": "document",
            "name": "nav data",
            "version": "1.0",
            }
        ];

        db.all(`SELECT waypoint_id, ident, lonx, laty FROM waypoint WHERE region='VH'`, [], (err, waypoints) => {
            if (err){
                console.log(err);
            }
            waypoints.forEach(data => {
                const waypoint = {
                    "id": data.waypoint_id,
                    "name": data.ident,
                    "position": {
                        "cartographicDegrees": [data.lonx, data.laty, 0]
                    },
                    "point": {"pixelSize": 5},
                    "label": {
                        "text": `${data.ident}`,
                        "font": "9px sans-serif",
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {
                            "cartesian2": [10, 15],
                        },
                        "distanceDisplayCondition": {
                            "distanceDisplayCondition": [0, 1000000]
                        },
                        "showBackground": true,
                        "backgroundColor": {
                            "rgba": [0, 0, 0, 100]
                        }
                    }
                }
                document.push(waypoint);
            })
            // console.log(document);
           callback(document);
        })

        db.all(`SELECT * FROM boundary WHERE name LIKE '%HONG KONG%'`, [], (err, boundary) => {
            if (err){
                console.log(err);
            }
            console.log(boundary[0].geometry.toString('bin'));
        })
    }
}