const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const http = require('http');
const server = http.createServer(app);
const io = require('socket.io')(server, {
  cors: {
    methods: ['GET', 'POST'],
  },
});

const realtime = require('./src/models/realtime');

const PORT = process.env.PORT || 5000;
// require('./src/database');

//Express config
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(cors());

app.get('/', (req, res) => {
  res.send("Hello World ! ");
});

// Handle client socket connection
io.on('connection', socket => {
  console.log('New client connected!');

  socket.on('disconnect', () => {
    console.log('user disconnected');
  })
})

setInterval(realtime.realtime, 5000, io.sockets, http);

server.listen(PORT, () => {
  console.log(`Server Listening on ${PORT}`);
});