var canvas;
var score;
var button;
var initialInput;
var submitButton;
var database;
var id = 0;
var count = 0;
var time = 0;

function setup() {
  canvas = createCanvas(1, 1);
  score = 0;
  
  var config = {
    apiKey: "AIzaSyCE_8CVn1Zio1f-EXpEgZtp-8aoyxpteVk",
    authDomain: "bestcamera-7e901.firebaseapp.com",
    databaseURL: "https://bestcamera-7e901.firebaseio.com",
    projectId: "bestcamera-7e901",
    storageBucket: "bestcamera-7e901.appspot.com",
    messagingSenderId: "1087271452402",
    appId: "1:1087271452402:web:9c34a3417a21237ebe5a6b",
    measurementId: "G-3J20J96NZX"

  };
  firebase.initializeApp(config);
  database = firebase.database();

  var ref = database.ref('jale');
  ref.on('value',gotData,errData);
} 

function gotData(data){
  console.log(data.val());
  var keys = Object.keys(data.val());
  var scores = data.val();

  var k = keys[keys.length-1]; 
  var name = scores[k].initials;
  console.log(scores[k].faceURL);
  if(time == 0 ){
	time++;
  } else printPersonData(scores,k);
}


function errData(err){
  console.log('Jale..');
  console.log(err);
}

function printPersonData(scores, k){
  id++;
  count++;
  if(count==18)
  {
	$('#alert_log > .row').slice(-3).remove();
	count-=3;
  }
  var initial = scores[k].initials;
  var febra = scores[k].febra;
  var pericol = scores[k].pericol;
  var faceURL = scores[k].faceURL;
  $('#remove_this').hide();
  $('#alert_log').prepend('<div class="col-md-4"><div class="latest text_align_center"><figure><img src="' +  faceURL + '" alt="#"/></figure><div class="nostrud"><h3>Cazul ' +  id + '</h3><p><strong>Mască:</strong> ' +  initial + '<br><strong>Febră:</strong> ' +  febra + '<br><strong>Pericol:</strong> ' +  pericol + '<br></p></div></div></div>')
}