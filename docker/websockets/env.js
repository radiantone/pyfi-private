/** InfluxDB v2 URL */
const url = process.env['INFLUX_URL'] || 'http://localhost:8086'
/** InfluxDB authorization token */
const token = process.env['INFLUX_TOKEN'] || 'HlHFsGBHW5-az41oOAoRSfbG6au_PBd-ZIPqZtnAXcmgUe3uJajiaKUznccBG2gqOP9wzBxCluZ1rKBqNHNj6Q=='
/** Organization within InfluxDB  */
const org = process.env['INFLUX_ORG'] || 'pyfi'
/**InfluxDB bucket used in examples  */
const bucket = 'pyfi'
// ONLY onboarding example
/**InfluxDB user  */
const username = 'admin'
/**InfluxDB password  */
const password = 'password'

module.exports = {
  url,
  token,
  org,
  bucket,
  username,
  password,
}
