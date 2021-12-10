var redis = require('ioredis');
var subscriber = redis.createClient();
subscriber.on('message', function (channel, message) {
 console.log('Message: ' + message + ' on channel: ' + channel + ' is arrive!');
});
subscriber.subscribe('notification');
