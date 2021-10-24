import socketIOClient from 'socket.io-client';

let socket = socketIOClient('/', {path: '/socket/', transports: ['websocket', 'polling', 'flashsocket']});

export default socket;