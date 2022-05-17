/** InfluxDB v2 URL */
const url = process.env['INFLUX_URL'] || 'http://localhost:8086'
/** InfluxDB authorization token */
//const token = process.env['INFLUX_TOKEN'] || 'M80QnDXESgPPsGqUMShtcWGORHUGZA6Z8jaPrPWAM1d16SLLWlAMHelVW2tt1rqudv-zD4Qw25AfN6VmwhpAwA=='
const token = process.env['INFLUX_TOKEN'] || 'PMmlw0KhdI1EyANBZwy9G0j-A2TyC3CIl7RnVTzaTx0bjmxGmpiU-KuuQm9U7ig-N3uCcHRWV2aDKJQLk6yKeg=='
/** Organization within InfluxDB  */
const org = process.env['INFLUX_ORG'] || 'elasticcode'
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
