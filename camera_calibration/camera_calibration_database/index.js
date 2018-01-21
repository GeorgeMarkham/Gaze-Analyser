const express = require('express');
var mongoose = require('mongoose');
var bodyParser = require('body-parser');
var app = express();

var port = 8080;

//Allow body parsing to get data
app.use(bodyParser.json());

mongoose.connect('mongodb://127.0.0.1:27017/camera_calibration_database')

//Define schema for camera calibration data
var camera_calibration_model = mongoose.model('camera_calibration_model', new mongoose.Schema({
    camera_name: String,
    mtx: [[Number]],
    dist: [[Number]]
}));


function getCameraData(cameraName){
    
}


app.get('/:camera_name', (req,res)=>{
    var cameraName = req.params.camera_name;
    camera_calibration_model.findOne({camera_name: cameraName}).exec((err, camera_calibration_data)=>{
        if(err){
            console.log(err);
            throw err;
            res.send("Couldn't find " + cameraName + " sorry!");
        } else {
            if(camera_calibration_data != null){
                console.log(camera_calibration_data);
                res.json(camera_calibration_data);
            }
        }
    })
})

app.post('/:camera_name', (req,res)=>{
    var cameraName = req.params.camera_name;
    var cameraMtx = req.body.mtx;
    var cameraDist = req.body.dist;

    var camera_calibration_entry = new camera_calibration_model({
        camera_name: cameraName,
        mtx: cameraMtx,
        dist: cameraDist
    });
    camera_calibration_entry.save((err)=>{
        if(err){
            console.log(err);
            throw err;
        } else {
            console.log("Added:" + cameraName + " to the database");
            res.send("Added:" + cameraName + " to the database, thanks for your help!");
        }
    });

})

app.listen(port, ()=>{
    console.log('listening on http://localhost:' + port);
})