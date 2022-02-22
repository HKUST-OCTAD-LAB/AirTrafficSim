const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');
const { spawn } = require('child_process');
const Tail = require('tail').Tail;

module.exports = {
    simulation: simulation = (res) => {
        console.log("function - simulation");

        const python = spawn('python', ['../simulation', '--headless']);

        python.stdout.on('data', function (data) {
            // console.log(data.toString());
        });

        python.stderr.on('data', function (data) {
            console.log(data.toString());
        });

        python.on('close', (code) => {
            console.log(`child process close all stdio with code ${code}`);

            const respond= []
            const document = []
            const data = []
            
            var alt = []
            var heading = []
            var cas = []
            var tas = []
            var mach = []
            var weight = []
            var fuel_weight = []
            var bank_angle = []
            var trans_alt = []
            var accel = []
            var drag = []
            var esf = []
            var thrust = []
            var flight_phase = []
            var speed_mode = []
            var ap_speed_mode = []

            var file_content = fs.readFileSync(`./data/simulation/simulation.csv`); //TODO: change to dynamic name
            const content = parse(file_content, {
                columns: true,
                skip_empty_lines: true
            });

            
            var positions = [];
            var label = [];
            var alt_data = []
            var heading_data = []
            var cas_data = []
            var tas_data = []
            var mach_data = []
            var weight_data = []
            var fuel_weight_data = []
            var bank_angle_data = []
            var trans_alt_data = []
            var accel_data = []
            var drag_data = []
            var esf_data = []
            var thrust_data = []
            var flight_phase_data = []
            var speed_mode_data = []
            var ap_speed_mode_data = []

            var time = new Date();
            var max_id = -1
            var max_time = 0
            var current_time = 0

            // var temp = []

            content.forEach((data)=>{
                if(data.id > max_id){
                    positions.push([])
                    label.push([])
                    alt_data.push([])

                    max_id += 1
                } 
                if(data.time > max_time){
                    max_time = data.time
                }

                // CZML document
                positions[data.id].push(new Date(time.getTime() + data.time * 1000).toISOString(), data.long, data.lat, data.alt/3.2808)
                label[data.id].push({
                        "interval": new Date(time.getTime() + data.time*1000).toISOString() + '/' + new Date(time.getTime() + (data.time + 1)*1000).toISOString(),
                        "string": `${data.callsign}\n${Math.round(data.alt)}ft ${Math.round(data.cas)}kt\n${Math.round(data.heading)}deg`
                })  
                    
                // Create data array for plotting
                alt_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.alt)
                })

            })

            for(let i = 0; i <= max_id;  i++){
                // Data plotting
                alt.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: alt_data[i]
                })
                
                // CZML document
                document.push({
                    "id": i,
                    // "availability": `${time.toISOString()}/${new Date(time + 500).toISOString()}`,
                    "position": {
                        "cartographicDegrees": positions[i]
                    },
                    "point": {
                        "pixelSize": 5,
                        "color": {
                            "rgba": [39, 245, 106, 215]
                        }
                    },
                    "path": {
                        "leadTime": 0,
                        "trailTime": 20,
                        "distanceDisplayCondition": {
                            "distanceDisplayCondition": [0, 1000000]
                        },
                        // "resolution": 600.0,
                        // "material": {
                        //     "polylineDash": {}
                        // }
                    },
                    "label": {
                        "text": label[i],
                        "font": "9px sans-serif",
                        "horizontalOrigin": "LEFT",
                        "pixelOffset": {
                            "cartesian2": [20, 20],
                        },
                        "distanceDisplayCondition": {
                            "distanceDisplayCondition": [0, 1000000]
                        },
                        "showBackground": false,
                        "backgroundColor": {
                            "rgba": [0, 0, 0, 50]
                        }
                    }
                })
            }
            const document_info = {
                "id": "document",
                "name": "simulated trajectories",
                "version": "1.0",
                "clock": {
                    "interval": `${time.toISOString()}/${new Date(time.getTime() + max_time * 1000).toISOString()}`,
                    "currentTime": `${time.toISOString()}`
                }
            };
            document.unshift(document_info);
            data.push(alt)

            respond.push(document)
            respond.push(data)
            res.send(respond)
        });
    }
}
