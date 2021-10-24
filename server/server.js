const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const postRouter = require('./src/routes/post.router');
require('./src/database');
const PORT = 5000;

app.get('/', (req, res) => {
    res.send("Hello World ! ");
});

app.listen(PORT, function () {
    console.log(`Server Listening on ${PORT}`);
});



app.use(
  bodyParser.urlencoded({
    extended: true
  })
);
app.use(bodyParser.json());

app.use('/posts', postRouter);