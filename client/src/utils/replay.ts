import axios from "axios";

axios.defaults.baseURL = 'http://127.0.0.1:8000/api';

class Replay{
    static get_replay_dir(){
        axios.get("replay").then( res => {
            console.log("replay", res.data);
        }).catch(err => {
            console.log(err);
        })
    }
}

export default Replay;