/** var express = require('express'),
  app = express(),
  mongoose = require('mongoose'),
  Task = require('./api/models/newsModel'), //created model loading here
  bodyParser = require('body-parser');
  
// mongoose instance connection url connection
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/newsDB'); 


app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(function(req, res) {res.status(404).send({url: req.originalUrl + ' not found'})});

var routes = require('./api/routes/newsRoutes');
const { prototype } = require('stream');
routes(app);


app.get('/search', function (req, res) {
    console.log('hit the script');

    var spawn = require("child_process").spawn;

    var dataToSend = req.params;
    // spawn new child process to call the python script
    const python = spawn('python', ['/scripts/news-pipeline.py', req.params.topic, req.params.date]);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('pipe data from nlp script ...');
        dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataToSend);
    });
})

var server = app.listen(8081, function () {
    var port = server.address().port;
    var host = server.address().address;
    console.log("app listening at http://%s:%s", host, port);
 })
**/
var express = require('express');
var app = express();
var cors = require('cors')
bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


var corsOptions = {
    origin: 'http://localhost:8100',
    optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
    allowedHeaders: ['Origin', 'X-Requested-With', 'Content-Type', 'Accept']
}

setInterval(function () {
    var spawn = require("child_process").spawn;
    var process = spawn('python', ['./scripts/updateNews.py']);
 }, 60 * 60 * 1000);

app.options('/search', cors(corsOptions))

app.get('/search', cors(corsOptions), function (req, res) {

    var spawn = require("child_process").spawn;

    // spawn new child process to call the python script

    console.log(req.query.topic)
    console.log(req.query.date)

    var process = spawn('python', ['./scripts/news-pipeline.py', req.query.topic, req.query.date]);
    

    // collect data from script
    process.stdout.on('data', function (data) {
        console.log('pipe data from nlp script');
        res.send(JSON.parse(data));
    });
    process.on('error', function () {
        console.log("Failed to start child.");
    });
    process.on('close', function (code) {
        console.log('Child process exited with code ' + code);
        
    });
    
})

app.get('/techcrunch', cors(corsOptions), function (req, res) {
    const fs = require('fs')

    fs.readFile('./data/techcrunch.json', 'utf8' , (err, data) => {
        if (err) {
            console.log('Child process exited with code ' + err)
            res.send(err)
        }
        res.send(data)
    })
})
app.get('/nba', cors(corsOptions), function (req, res) {
    const fs = require('fs')

    fs.readFile('./data/nba.json', 'utf8' , (err, data) => {
        if (err) {
            console.log('Child process exited with code ' + err)
            res.send(err)
        }
        res.send(data)
    })
})
app.get('/nfl', cors(corsOptions), function (req, res) {
    const fs = require('fs')

    fs.readFile('./data/nfl.json', 'utf8' , (err, data) => {
        if (err) {
            console.log('Child process exited with code ' + err)
            res.send(err)
        }
        res.send(data)
    })
})
app.get('/nhl', cors(corsOptions), function (req, res) {
    const fs = require('fs')

    fs.readFile('./data/nhl.json', 'utf8' , (err, data) => {
        if (err) {
            console.log('Child process exited with code ' + err)
            res.send(err)
        }
        res.send(data)
    })
})

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port
   console.log("app listening at http://%s:%s", host, port)
})
