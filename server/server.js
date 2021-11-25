const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const server = require('http').createServer(app);
const io = require('socket.io')(server, {
  cors: {
    methods: ['GET', 'POST'],
  },
});


const PORT = process.env.PORT || 5000;
// require('./src/database');

//Express config
app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());
app.use(cors());

app.get('/', (req, res) => {
  res.send("Hello World ! ");
});

const json = require('./src/data/sample.json')

// Handle client socket connection
io.on('connection', socket => {
  console.log('New client connected!');

  socket.emit("realtime:all", json);

  socket.on('disconnect', () => {
    console.log('user disconnected');
  })
})

server.listen(PORT, () => {
  console.log(`Server Listening on ${PORT}`);
});