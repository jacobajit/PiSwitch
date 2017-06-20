// Copyright 2016, Google, Inc.
// Licensed under the Apache License, Version 2.0 (the 'License');
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an 'AS IS' BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

'use strict';

//var requestModule = require('request');

var http = require('http');
var options = {
  host: 'pubsub.pubnub.com',
  path: '/publish/pub-c-6e839019-682d-44bf-9f0a-1f15abd00dc8/sub-c-c72d9fd4-9212-11e6-a68c-0619f8945a4f/0/gpio-raspberry-control/0/%7B%20%22req%22%20:%20%22toggle%22%20%7D'
};

process.env.DEBUG = 'actions-on-google:*';
const App = require('actions-on-google').ApiAiApp;
const functions = require('firebase-functions');

// API.AI actions
const TELL_FACT = 'tell.fact';

var req = http.get(options, function(res) {
  console.log('STATUS: ' + res.statusCode);
  console.log('HEADERS: ' + JSON.stringify(res.headers));

  // Buffer the body entirely for processing as a whole.
  var bodyChunks = [];
  res.on('data', function(chunk) {
    // You can process streamed parts here...
    bodyChunks.push(chunk);
  }).on('end', function() {
    var body = Buffer.concat(bodyChunks);
    console.log('BODY: ' + body);
    // ...and/or process the entire body here.
  })
});

req.on('error', function(e) {
  console.log('ERROR: ' + e.message);
});
console.log('Does it ever reach here?');

exports.factsAboutGoogle = functions.https.onRequest((request, response) => {
  const app = new App({ request, response });
  console.log('Request headers: ' + JSON.stringify(request.headers));
  console.log('Request body: ' + JSON.stringify(request.body));

  // Say a fact
  function tellFact (app) {
    //requestModule('http://pubsub.pubnub.com/publish/pub-c-6e839019-682d-44bf-9f0a-1f15abd00dc8/sub-c-c72d9fd4-9212-11e6-a68c-0619f8945a4f/0/gpio-raspberry-control/0/%7B%20%22req%22%20:%20%22toggle%22%20%7D', function (error, response, body) {
    //requestModule('tinyurl.com/piswitch', function (error, response, body) {
    //  console.log('error:', error); // Print the error if one occurred 
    //  console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received 
    //  console.log('body:', body); // Print the HTML for the Google homepage. 
    //});
    var req = http.get(options, function(res) {
      console.log('STATUS: ' + res.statusCode);
      console.log('HEADERS: ' + JSON.stringify(res.headers));

      // Buffer the body entirely for processing as a whole.
      var bodyChunks = [];
      res.on('data', function(chunk) {
        // You can process streamed parts here...
        bodyChunks.push(chunk);
      }).on('end', function() {
        var body = Buffer.concat(bodyChunks);
        console.log('BODY: ' + body);
        // ...and/or process the entire body here.
      })
    });

    req.on('error', function(e) {
      console.log('ERROR: ' + e.message);
    });
    app.ask('Does it ever reach here?');
  }

  let actionMap = new Map();
  actionMap.set(TELL_FACT, tellFact);

  app.handleRequest(actionMap);
});
