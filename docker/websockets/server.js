const WebSocket = require('ws');
const redis = require('ioredis');

// Configuration: adapt to your environment
const REDIS_SERVER = "redis://redis:6379";
const WEB_SOCKET_PORT = 3000;

var redisClient = redis.createClient(REDIS_SERVER);

redisClient.on('message', function(channel, message){
  console.log(message);
});


console.log("Subscribing to channel ",process.env.PYFI_CHANNEL)
redisClient.subscribe(process.env.PYFI_CHANNEL);
// sqlalchemy get all the stored processors and subscribe to them

// Create & Start the WebSocket server
const server = new WebSocket.Server({ port : WEB_SOCKET_PORT });

console.log("Configured subscription")
// Register event for client connection
server.on('connection', function connection(ws) {
  console.log("User connected");

  // broadcast on web socket when receving a Redis PUB/SUB Event
  redisClient.on('message', function(channel, message){
    console.log(message);
    ws.send(message);
    // Send message to influxdb using current timestamp?
  })

});

console.log("WebSocket server started at ws://localhost:"+ WEB_SOCKET_PORT);
