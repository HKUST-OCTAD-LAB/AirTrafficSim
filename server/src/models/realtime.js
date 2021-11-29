module.exports = {
    realtime: realtime = (socket, http) => {
        console.log("function - realtime");
        http.request("http://data-live.flightradar24.com/zones/fcgi/feed.js?faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&gliders=1&stats=1", (res) => {
            var data = "";
            res.on("data", (chunk) => {
                data += chunk;
            });
            res.on("end", () => {
                let content = JSON.parse(data);
                delete content.version;
                delete content.full_count;
                delete content.stats;

                var time = new Date();
                console.log(time.toISOString());
                const aircrafts = [
                    {
                        "id": "document",
                        "name": "My Document",
                        "version": "1.0",
                        // "clock": {
                        //     "currentTime": time.toISOString()
                        // }
                    }
                ];

                Object.keys(content).forEach((key) => {
                    const aircraft = {
                        "id": key,
                        "name": content[key][13],
                        "description": `${content[key][2]}, ${content[key][1]}, ${content[key][4]}`,
                        "epoch": time.toISOString(),
                        "position": {
                            "cartographicDegrees": [content[key][2], content[key][1], content[key][4]]
                        },
                        "point": {"pixelSize": 5},
                        "label": {
                            "text": `${content[key][2]}, ${content[key][1]}, ${content[key][4]}`,
                            "font": "1px",
                            "horizontalOrigin": "LEFT",
                            "pixelOffset": {
                                "cartesian2": [8, 0],
                            },
                            "distanceDisplayCondition": {
                                "distanceDisplayCondition": [0, 2000000]
                            },
                        }
                    }
                    aircrafts.push(aircraft);
                });
 
                socket.volatile.emit("realtime:all", aircrafts); 
            });
        }).end();

        

        // fs.readdir('./data/20180701/', (err, files) => {
        //     files.forEach(file => {
        //         console.log(file);
        //         var file_content = fs.readFileSync('./data/20180701/' + file);
        //         let content = JSON.parse(file_content);
        //     })
        // })
    }
}
