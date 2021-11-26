const fs = require('fs');

module.exports = {
    raeltime: realtime = () => {
        console.log("realtime");

        var time = new Date().toISOString;
        var file_content = fs.readFileSync('./data/20180701/fr24_China_20180701_Sun_2353_1.json');
        let content = JSON.parse(file_content);
        delete content.version;
        delete content.full_count;
        const aircrafts = [
            {
                "id": "document",
                "name": "My Document",
                "version": "1.0",
                "clock": {
                    "currentTime": time
                }
            }
        ];
        Object.keys(content).forEach(function(key) {
            const aircraft = {
                "id": content[key][13],
                epoch: time,
                "position": {"cartographicDegrees": [content[key][2], content[key][1], content[key][4]]},
                "point": {"pixelSize": 3}
            }
            aircrafts.push(aircraft);
        });
        console.log(aircrafts);
        return (aircrafts);

        // fs.readdir('./data/20180701/', (err, files) => {
        //     files.forEach(file => {
        //         console.log(file);
        //         var file_content = fs.readFileSync('./data/20180701/' + file);
        //         let content = JSON.parse(file_content);
        //     })
        // })
    }
}
