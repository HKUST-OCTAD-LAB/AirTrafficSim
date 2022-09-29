import { io } from "socket.io-client";

const socket = io("http://localhost:6111");

export default socket;