const express = require('express');
const bodyParser = require('body-parser');
const postRouter = require('./src/routes/post.router');
const cors = require('cors');
const { Server } = require("socket.io");
const http = require('http');
// require('./src/database');
const PORT = 5000;

const app = express();

app.use(
  bodyParser.urlencoded({
    extended: true
  })
);
app.use(bodyParser.json());
app.use(cors());

app.get('/', (req, res) => {
  res.send("Hello World ! ");
});

app.listen(PORT, function () {
  console.log(`Server Listening on ${PORT}`);
});

const server = http.createServer(app);
const io = new Server(server);

io.on('connection', socket => {
  console.log('New client connected!');
  
  socket.broadcast.emit('hi');

  socket.on('abc', (msg) => {
    io.emit('abc', msg);
  });

  socket.on('disconnect', () => {
    console.log('user disconnected');
  })
})