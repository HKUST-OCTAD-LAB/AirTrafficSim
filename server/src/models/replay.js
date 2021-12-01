const fs = require('fs');

module.exports = {
    replay: replay = (req) => {
        const trajectories = [];
        var startTime, endTime = undefined;
        fs.readdirSync("./data/historic/").forEach((file) => {
            var file_content = fs.readFileSync(`./data/historic/${file}`);
            let content = JSON.parse(file_content);
            var start = content[0].timestamp * 1000;
            var end = content[content.length-1].timestamp * 1000;
            console.log(startTime, endTime, start, end);
            if (startTime == undefined || endTime == undefined){
                startTime = start;
                endTime = end;
            }
            if (start <  startTime){
                startTime = start;
                console.log("start < startTime");
            }
            if (end > endTime){
                endTime = end;
                console.log("end > endTime");
            }

            var positions = [];
            content.forEach((data)=>{
                positions.push(new Date(data.timestamp * 1000).toISOString(), data.long, data.lat, data.alt/3.2808)
            })
            const trajectory = {
                "id": file,
                "availability": `${new Date(start).toISOString()}/${new Date(end).toISOString()}`,
                "position": {
                    "cartographicDegrees": positions
                },
                "point": {
                    "pixelSize": 10,
                    "color": {
                        "rgba": [39, 245, 106, 215]
                    }
                },
                "path": {
                    "trailTime":0
                }
            }
            trajectories.push(trajectory);
        })

        const document = {
            "id": "document",
            "name": "simulated trajectories",
            "version": "1.0",
            "clock": {
                "interval": `${new Date(startTime).toISOString()}/${new Date(endTime).toISOString()}`,
                "currentTime": `${new Date(startTime).toISOString()}`
            }
        }
        trajectories.unshift(document);
        return trajectories;
    }
}