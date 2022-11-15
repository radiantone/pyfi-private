const SwaggerParser = require('@apidevtools/swagger-parser')

let get = async () => {
    try {
      const api = await SwaggerParser.validate('https://apitools.dev/swagger-parser/online/sample/swagger.yaml')
      console.log('API name: %s, Version: %s', api.info.title, api.info.version)
      return api
    } catch (err) {
      console.error(err)
    }
}


get().then( (api) => {
console.log(api)
// Generate python client wrappers 
 for(var path in api.paths) {
   let pathobj = api.paths[path]
   let _path = path.replace(/}/gm,'')
   _path = _path.replace(/\/{/gm,'_')
   _path = _path.replace('/','_')
   let func = "def "
   for(var method in pathobj) {
     func = func + method+_path 
     let params = pathobj[method]["parameters"]
     if (method === "get") {
        func += "("
	for (let index in params) {
         let param = params[index]
	 func = func + param.name
         if (index+1 < params.length) {
           func = func + ","
         }
        }
       func = func + "):\n"
       func = func + "    # subs params into url+path\n"
       func = func + "    # http.get(url)\n"
       func = func + "    pass\n\n"
       console.log(func)
     }
   }
 }
// For each endpoint, convert to this_is_the_endpoint(arg1, arg2)
// where arg1, arg2 are named variables in the route {arg1} {arg2}
// for each parameter in parameters
// if in==path, then parse out {param}
// if in==body, then add argument to accept body

// Set title, description of block from API spec
})
