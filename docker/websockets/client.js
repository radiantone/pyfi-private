const WebSocket = require('ws')
 
const {InfluxDB, Point, HttpError} = require('@influxdata/influxdb-client')
const {url, token, org, bucket} = require('./env')
const {hostname} = require('os')

// Docker redis subscribe to websocket service is running
const wsurl = 'ws://localhost:3000'
const connection = new WebSocket(wsurl)
// create a write API, expecting point timestamps in nanoseconds (can be also 's', 'ms', 'us')
const writeApi = new InfluxDB({url, token}).getWriteApi(org, bucket, 'ns')
// setup default tags for all writes through this API
writeApi.useDefaultTags({ location: hostname() })

connection.onopen = () => {
  connection.send('Message From Client') 
}
 
connection.onerror = (error) => {
  console.log(`WebSocket error: ${error}`)
}
 
connection.onmessage = (e) => {
  var msg = JSON.parse(e.data)

  if (msg.hasOwnProperty('message')) {
    var graph = JSON.parse(msg['message'])
    console.log(graph)
    if (graph.hasOwnProperty('message')) {
      
    var graph = JSON.parse(graph['message'].slice(1,-1).replace(/\\n/g, '').replace(/\\/g, ''))
      console.log("Inner message", graph)
      if (graph.graph) {
        const point1 = new Point(graph.graph.name)
          .tag('type',graph.graph.name)
          .floatField('value', parseFloat(graph.graph.value))
          .timestamp(new Date())
      
        console.log("point1",point1);
        writeApi.writePoint(point1)
        writeApi.flush()
      }
    }
    console.log("Wrote to influxdb");
  }
}





// write point with the current (client-side) timestamp


// WriteApi always buffer data into batches to optimize data transfer to InfluxDB server and retries
// writing upon server/network failure. writeApi.flush() can be called to flush the buffered data,
// close() also flushes the remaining buffered data and then cancels pending retries.
/*
writeApi
  .close()
  .then(() => {
    console.log('FINISHED ... now try ./query.ts')
  })
  .catch(e => {
    console.error(e)
    if (e instanceof HttpError && e.statusCode === 401) {
      console.log('Run ./onboarding.js to setup a new InfluxDB database.')
    }
    console.log('\nFinished ERROR')
  })*/
