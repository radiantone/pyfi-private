/** InfluxDB v2 URL */
const url = process.env['INFLUX_URL'] || 'http://localhost:8086'
/** InfluxDB authorization token */
const token = process.env['INFLUX_TOKEN'] || 'M80QnDXESgPPsGqUMShtcWGORHUGZA6Z8jaPrPWAM1d16SLLWlAMHelVW2tt1rqudv-zD4Qw25AfN6VmwhpAwA=='
/** Organization within InfluxDB  */
const org = process.env['INFLUX_ORG'] || 'pyfi'
/**InfluxDB bucket used in examples  */
const bucket = 'pyfi'
// ONLY onboarding example
/**InfluxDB user  */
const username = 'admin'
/**InfluxDB password  */
const password = 'DGRacing56'

module.exports = {
  url,
  token,
  org,
  bucket,
  username,
  password,
}
