const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require("path");

const app = express();
const http = require('http');
const server = http.createServer(app);
const io = require('socket.io')(server, {
  cors: {
    methods: ['GET', 'POST'],
  },
});

const realtime = require('./src/models/realtime');
const replay = require('./src/models/replay');
const navdata = require('./src/models/navdata');
const simulation = require('./src/models/simulation')

const PORT = process.env.PORT || 5000;
// require('./src/database');

//Express config
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(cors());

app.use(express.static("../client/build"));

app.get('/replay', (req, res) => {
  res.send(replay.replay());
})

app.get('/navdata', (req, res) => {
  // const sendnav = (document) => {
  //   res.send(document);
  // }

  // navdata.navdata(sendnav);
})

app.get('/api/simulation', (req, res) => {
  simulation.simulation(res);
  // simulation.simulation(io.socket)
})

// Handles any requests that don't match the ones above
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, "../client/build", "index.html"));
});

// Handle client socket connection
io.on('connection', socket => {
  console.log('New client connected!');

  socket.on('disconnect', () => {
    console.log('user disconnected');
  })
})

// setInterval(realtime.realtime, 2000, io.sockets, http);

// tail.on("line", function(data) {
//   console.log(data);
// });

server.listen(PORT, () => {
  console.log(`Server Listening on ${PORT}`);
});