const SwaggerParser = require('@apidevtools/swagger-parser')

let get = async () => {
  try {
    const api = await SwaggerParser.validate('https://petstore.swagger.io/v2/swagger.json')
    console.log('API name: %s, Version: %s', api.info.title, api.info.version)
    return api
  } catch (err) {
    console.error(err)
  }
}


get().then((api) => {
  console.log(api)
  // Generate python client wrappers
  console.log("url = 'https://"+api.host+api.basePath+"'")
  let code = ''
  for (var path in api.paths) {
    let pathobj = api.paths[path]
    let _path = path.replace(/}/gm, '')
    _path = _path.replace(/\/{/gm, '_')
    _path = _path.replace(/\//gm, '_')
    for (var method in pathobj) {
      let func = "def " + method + _path
      let params = pathobj[method]["parameters"]
      func += "("
      for (let index in params) {
        let param = params[index]
        func = func + param.name
        if (parseInt(index) < params.length-1) {
          func = func + ","
        }
      }
      func = func + "):\n"
      func = func + "    from pyodide.http import pyfetch\n"
      func = func + "    import json\n"
      func = func + "    data = json.dumps({'this':'that'})\n"
      func = func + "    response = pyfetch(url+f\""+path+"\", mode=\"cors\", cache=\"no-cache\", credentials=\"same-origin\", headers={'Content-Type': 'application/json'}, body=data, method=\""+method.toUpperCase()+"\")\n\n"
      code = code + func
    }
  }
// For each endpoint, convert to this_is_the_endpoint(arg1, arg2)
// where arg1, arg2 are named variables in the route {arg1} {arg2}
// for each parameter in parameters
// if in==path, then parse out {param}
// if in==body, then add argument to accept body
console.log(code)
// Set title, description of block from API spec
})
