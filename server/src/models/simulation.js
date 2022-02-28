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
            console.log(data.toString());
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
            var vs = []
            var weight = []
            var fuel_consumed = []
            var bank_angle = []
            var trans_alt = []
            var accel = []
            var drag = []
            var esf = []
            var thrust = []
            var flight_phase = []
            var speed_mode = []
            var ap_speed_mode = []

            var file_content = fs.readFileSync(`../data/simulation/simulation.csv`); //TODO: change to dynamic name
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
            var vs_data = []
            var weight_data = []
            var fuel_consumed_data = []
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

            content.forEach((data)=>{
                if(data.id > max_id){
                    positions.push([])
                    label.push([])
                    alt_data.push([])
                    heading_data.push([])
                    cas_data.push([])
                    tas_data.push([])
                    mach_data.push([])
                    vs_data.push([])
                    weight_data.push([])
                    fuel_consumed_data.push([])
                    bank_angle_data.push([])
                    trans_alt_data.push([])
                    accel_data.push([])
                    drag_data.push([])
                    esf_data.push([])
                    thrust_data.push([])
                    flight_phase_data.push([])
                    speed_mode_data.push([])
                    ap_speed_mode_data.push([])

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

                heading_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.heading)
                })

                cas_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.cas)
                })

                tas_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.tas)
                })

                mach_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.mach)
                })

                vs_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.vs)
                })

                weight_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.weight)
                })

                fuel_consumed_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.fuel_consumed)
                })

                bank_angle_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.bank_angle)
                })

                trans_alt_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.trans_alt)
                })

                accel_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.accel)
                })

                drag_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.drag)
                })

                esf_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.esf)
                })

                thrust_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.thrust)
                })

                flight_phase_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.flight_phase)
                })

                speed_mode_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.speed_mode)
                })

                ap_speed_mode_data[data.id].push({
                    time: Number(data.time),
                    value: Number(data.ap_speed_mode)
                })
            })

            for(let i = 0; i <= max_id;  i++){
                // Data plotting
                alt.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: alt_data[i]
                })

                heading.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: heading_data[i]
                })

                cas.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: cas_data[i]
                })

                tas.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: tas_data[i]
                })

                mach.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: mach_data[i]
                })

                vs.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: vs_data[i]
                })

                weight.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: weight_data[i]
                })

                fuel_consumed.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: fuel_consumed_data[i]
                })

                bank_angle.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: bank_angle_data[i]
                })

                trans_alt.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: trans_alt_data[i]
                })

                accel.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: accel_data[i]
                })

                drag.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: drag_data[i]
                })

                esf.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: esf_data[i]
                })

                thrust.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: thrust_data[i]
                })

                flight_phase.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: flight_phase_data[i]
                })

                speed_mode.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: speed_mode_data[i]
                })

                ap_speed_mode.push({
                    id: content[i].id,
                    name: content[i].callsign,
                    data: ap_speed_mode_data[i]
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
                            "distanceDisplayCondition": [0, 1500000]
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
                            "distanceDisplayCondition": [0, 1500000]
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
            data.push(alt);
            data.push(heading);
            data.push(cas);
            data.push(tas);
            data.push(mach);
            data.push(vs);
            data.push(weight);
            data.push(fuel_consumed);
            data.push(bank_angle);
            data.push(trans_alt);
            data.push(accel);
            data.push(drag);
            data.push(esf);
            data.push(thrust);
            data.push(flight_phase);
            data.push(speed_mode);
            data.push(ap_speed_mode);

            respond.push(document);
            respond.push(data);
            res.send(respond);
        });
    }
}
