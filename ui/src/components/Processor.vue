<script lang="ts">
/* eslint-disable @typescript-eslint/no-unsafe-assignment,@typescript-eslint/no-unsafe-call */
import Vue from 'vue'
import mixins from 'vue-typed-mixins'
import { Wrapper } from '../util'
import { io, Socket } from 'socket.io-client'
import { parseCronExpression, IntervalBasedCronScheduler } from 'cron-schedule'
import Moment from 'moment/moment'
import DataService from 'components/util/DataService'

let scheduler

const GUEST = 0
const FREE = 1
const DEVELOPER = 2
const PRO = 3
const HOSTED = 4
const ENTERPRISE = 5

const toObject = (map : any): any => {
  if (!(map instanceof Map)) return map
  return Object.fromEntries(Array.from(map.entries(), ([k, v]) => {
    if (v instanceof Array) {
      return [k, v.map(toObject)]
    } else if (v instanceof Map) {
      return [k, toObject(v)]
    } else {
      return [k, v]
    }
  }))
}

interface ServerToClientEvents {
  noArg: () => void;
  basicEmit: (a: number, b: string, c: Buffer) => void;
  global: (data: any) => void;
  execute: (data: any) => void;
  withAck: (d: string, callback: (e: number) => void) => void;
}

interface ClientToServerEvents {
  hello: (data: SocketData) => void;
}

interface SocketData {
  name: string;
  age: number;
}

export interface ProcessorState {
  name: string;
  id: string;
  interval: number;
  scheduler: any;

  obj: any;
  middlewareonly: boolean;
  usemiddleware: boolean;
  middleware: string;
  middlewarefunc: string;
  sublevel: { [key: string]: any };

  environment: { [key: string]: any };
  portobjects: { [key: string]: any };
  argobjects: { [key: string]: any };
  errorobjects: { [key: string]: any };
  tasks: any[];
}

export const ProcessorMixin = Vue.extend({
  data () {
    return {
      sublevel: {},
      name: 'Processor',
      portobjects: {},
      middlewareonly: true,
      usemiddleware: false,
      middlewarefunc: '',
      obj: {},
      environment: {},
      middleware: '## middleware will receive the input, make API call to database service, receive output and pass it along\n',
      argobjects: {},
      errorobjects: {}
    }
  }
})

export class ProcessorBase extends ProcessorMixin implements ProcessorState {
  name!: ProcessorState['name'];
  id!: ProcessorState['id'];
  middlewareonly!: ProcessorState['middlewareonly'];
  usemiddleware!: ProcessorState['usemiddleware'];
  middlewarefunc!: ProcessorState['middlewarefunc'];
  middleware!: ProcessorState['middleware'];

  environment!: ProcessorState['environment'];
  interval!: ProcessorState['interval'];

  obj!: ProcessorState['obj'];
  scheduler!: ProcessorState['scheduler'];
  sublevel!: ProcessorState['sublevel'];
  tasks!: ProcessorState['tasks'];
}

const socketserver = <string>process.env.SOCKETIO

const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(
  socketserver
)

const mapToObj = (m: Map<string, any>) => {
  return Array.from(m).reduce((obj: { [name: string]: any }, [key, value]) => {
    obj[key] = value
    return obj
  }, {})
}

interface ProcessorInterface {
  messageReceived(message: any): void;
  getVersion(): string;
  messageSend(message: any): void;
  getPort(func: string, name: string): any;
  listenMessages(): void;
  setId(id: string): void;
  execute(data: any): void;
  startSchedule(cron: string): void;
  stopSchedule(): void;
}

type Methods = ProcessorInterface

let includes = ''

interface Computed {
}

interface Props {
  wrapper: Wrapper;
}

export default mixins(ProcessorBase).extend<ProcessorState,
  Methods,
  Computed,
  Props>({
    data () {
      return {
        scheduler: null,
        interval: -1,
        tasks: [],
        name: 'MyProcessor',
        id: 'any',
        middlewareonly: true,
        usemiddleware: false,
        middlewarefunc: '',
        middleware: '## middleware will receive the input, make API call to database service, receive output and pass it along\n',
        sublevel: {},
        environment: {},
        portobjects: {},
        obj: {},
        argobjects: {},
        errorobjects: {}
      }
    },

    created () {
      var me = this

      includes = 'from pyodide.http import pyfetch, FetchResponse\n' +
  'from typing import Optional, Any\n' +
  '\n' +
  'async def request(url: str, method: str = "GET", body: Optional[str] = None,\n' +
  '                  headers: Optional[dict[str, str]] = None, **fetch_kwargs: Any) -> FetchResponse:\n' +
  '    """\n' +
  '    Async request function. Pass in Method and make sure to await!\n' +
  '    Parameters:\n' +
  '        url: str = URL to make request to\n' +
  '        method: str = {"GET", "POST", "PUT", "DELETE"} from `JavaScript` global fetch())\n' +
  '        body: str = body as json string. Example, body=json.dumps(my_dict)\n' +
  '        headers: dict[str, str] = header as dict, will be converted to string...\n' +
  '            Example, headers=json.dumps({"Content-Type": "application/json"})\n' +
  '        fetch_kwargs: Any = any other keyword arguments to pass to `pyfetch` (will be passed to `fetch`)\n' +
  '    Return:\n' +
  '        response: pyodide.http.FetchResponse = use with .status or await.json(), etc.\n' +
  '    """\n' +
  '    headers = {"Authorization":"Bearer ' + this.$store.state.designer.token + '", "Content-type": "application/json"}\n' +
  '    kwargs = {"method": method, "mode": "cors"}  # CORS: https://en.wikipedia.org/wiki/Cross-origin_resource_sharing\n' +
  '    if body and method not in ["GET", "HEAD"]:\n' +
  '        kwargs["body"] = body\n' +
  '    if headers:\n' +
  '        kwargs["headers"] = headers\n' +
  '    kwargs.update(fetch_kwargs)\n' +
  '\n' +
  '    response = await pyfetch(url, **kwargs)\n' +
  '    return response' +
  '\n'

      socket.on('basicEmit', (a, b, c) => {
        if (me.$store) {
          me.$store.commit('designer/setMessage', b)
        }
      })
      me.listenMessages()
      me.sublevel = {
        guest: 0,
        free: 1,
        'ec_developer-USD-Monthly': 2,
        'ec_pro-USD-Monthly': 3,
        'ec_hosted-USD-Yearly': 4
      }
    },
    watch: {
      interval: function (newv, oldv) {
        //
      },
      connected: function (newv, oldv) {
        console.log('PROCESSOR CONNECTED', oldv, newv)
        if (newv) {
        // This means that changes to the flow are committed back
        // to the database as they happen
        }
      },
      streaming: function (newv, oldv) {
        console.log('PROCESSOR STREAMING', oldv, newv)
        if (newv) {
        // This means the flow is receiving streaming messages in real-time
          console.log('PROCESSOR: Turning on messages')
        } else {
          socket.off('global')
          console.log('PROCESSOR:  Turning off messages')
        }
      }
    },
    // eslint-disable-next-line @typescript-eslint/no-empty-function
    mounted () {

    },
    computed: {
      hasHosted () {
        if (this.$store.state.designer.subscription) {
          return this.sublevel[this.$store.state.designer.subscription] >= HOSTED
        } else {
          return false
        }
      }
    },
    methods: {
      getVersion () {
        if (this.$store.state.designer.version.indexOf('Free') >= 0) {
          return 'FREE'
        } else {
          return 'DEV'
        }
      },
      stopSchedule () {
        console.log('stopSchedule')
        this.scheduler.stop()
      },
      startSchedule (cronstr: string) {
        var me = this
        console.log('startSchedule')
        scheduler = new IntervalBasedCronScheduler(this.interval)
        scheduler.stop()
        const cron = parseCronExpression(cronstr)
        scheduler.registerTask(cron, () => {
          me.$emit('message.received', {
            type: 'trigger'
          })
        })
        this.scheduler = scheduler
        scheduler.start()
      },
      getPort (func: string, name: string) {
        for (var i = 0; i < this.portobjects[func].length; i++) {
          const port = this.portobjects[func][i]

          if (port.name === name) {
            return port
          }
        }
        return null
      },
      setId (id: string) {
        var me = this;

        (window as any).root.$off(id);
        (window as any).root.$on(id, async (code: string, func: string, argument: string, data: any, block: any, portname: string) => {
          let obj = data
          this.id = id

          // Set object based on its incoming type
          if (data instanceof Map) {
            obj = mapToObj(<Map<string, any>>data)
          } else if (data instanceof Object) {
            if (data.type && data.type === 'error') {
              obj = data
            } else {
              if ('toJs' in data) {
                obj = Object.fromEntries(data.toJs())
              }
            }
          }

          // TODO: This needs to be controlled by the block and the middleware, not heres
          const param = { data: obj, database: { table: argument, url: this.obj.connection, type: this.obj.database } }

          let param_string = JSON.stringify(param)

          if (me.usemiddleware) {
            console.log('RUN MIDDLEWARE', func, argument, obj, me.middlewarefunc, me.middleware)

            const _ = (window as any).pyodide.runPython(includes)

            // TODO: Replace "run" with middleware function selected from config dropdown
            const mcode = me.middleware + '\n\n' + me.middlewarefunc + '(' + param_string + ')\n'
            console.log('CODE MIDDLEWARE', mcode)
            this.$emit('middleware.started', {
              portname:portname
            })
            const result = (window as any).pyodide.runPythonAsync(mcode)
            result.then((res: any) => {
              const jsonoutput = res.toJs()
              const _result = toObject(jsonoutput)
              console.log('RUN MIDDLEWARE RESULT', jsonoutput, _result, JSON.stringify(_result))
              this.$emit('message.received', {
                type: 'result',
                id: id,
                function: 'run',
                obj: obj,
                portname: portname,
                output: JSON.stringify(_result)
              })
            })
          }

          // Find the matching port receiving the call
          this.$emit('arg.in', obj)
          console.log('NODE DATA RECEIVED', id, func, argument, obj)
          let port = null
          let complete = false

          // TODO: This fails for database object
          if (func && me.portobjects[func]) {
            for (var i = 0; i < me.portobjects[func].length; i++) {
              if (me.portobjects[func][i].name === argument) {
                port = me.portobjects[func][i]
                port.data = obj
              }
            }
            console.log('PROCESSOR EXECUTING PORT', func, argument, data, port)

            // Determine if the port arguments are complete
            complete = true
            for (var i = 0; i < me.portobjects[func].length; i++) {
              const port = me.portobjects[func][i]
              if (port.data === undefined || port.data === null) {
                complete = false
                break
              }
            }
          } else {
            if (func === undefined) {
              console.log('MIDDLEWARE', this.usemiddleware, this.middlewareonly)
              if (this.usemiddleware && this.middlewareonly) {
                console.log('NO FUNCTION, CALLING MIDDLEWARE ONLY', me.middlewarefunc, this.middleware)
                this.$emit('middleware.complete', {
                  type: 'middleware',
                  bytes: param_string.length,
                  portname: portname
                })
              }
            }
          }
          // Execute on port if complete
          console.log('COMPLETE', complete)
          if (complete) {
            console.log('FUNCTION', func, 'IS COMPLETE!')
            console.log('ENV', me.obj.variabledata)
            console.log('   INVOKING:', func, data)
            let call = func + '('

            let count = 0
            const argdata: any[] = []
            let funcargs: any = ''

            // For all ports associated with the requested function
            me.portobjects[func].forEach((_arg: any) => {
              let jsonarg = _arg.data

              argdata.push(jsonarg)
              // If we already have JSON encoded data, then pass it along
              // otherwise, convert it to JSON
              let isobj = false

              if (typeof jsonarg === 'string') {
                try {
                  JSON.parse(jsonarg)
                  isobj = true
                } catch (err) {
                  // Leave jsonarg as is, since the string is not JSON
                }
              } else {
                if (_arg.data instanceof Object) {
                  isobj = true
                  jsonarg = JSON.stringify(_arg.data)
                }
              }

              console.log('    ARG:', _arg, jsonarg)
              if (count > 0) {
                funcargs = funcargs + ','
              }

              // We have to double encode and decode the data because the raw
              // json output is not python object compatible. So we have to convert the raw
              // JSON result to a JSON string which can then be converted to a python object
              // with json.loads
              if (isobj) {
                funcargs = funcargs + 'json.loads(' + JSON.stringify(jsonarg) + ')'
              } else {
                funcargs = funcargs + jsonarg
              }
              count += 1
            })
            call = call + funcargs + ')'

            if (this.usemiddleware && !this.middlewareonly) {
              call = 'middleware  ( ' + call + ' )'
            } else if (this.usemiddleware && this.middlewareonly) {
              call = 'middleware  ( ' + funcargs + ' )'
            }

            console.log('FUNCTION CALL', call)
            console.log('CODE CALL', code + '\n' + call)
            var start = Moment(new Date())

            // Run in container
            if (block && block.container) {
              call = 'import json\n_result = ' + call
              console.log('RUN BLOCK IN CONTAINER', block)
              call = call + '\nprint(json.dumps(_result))\n'
              console.log('CODE CALL RUNBLOCK', code + '\n' + call)
              DataService.runBlock(block, call, this.$store.state.designer.token).then((result: any) => {
                console.log('CONTAINER RESULT', result)
                var end = Moment(new Date())
                const diff = end.diff(start)
                var time = Moment.utc(diff).format('HH:mm:ss.SSS')

                let answer = result.data
                try {
                  const parse = JSON.parse(result.data)
                  answer = parse
                } catch (error) {

                }

                let _plugs = {}
                if (answer.hasOwnProperty('plugs')) {
                  _plugs = answer.plugs
                }

                this.$emit('message.received', {
                  type: 'result',
                  id: this.id,
                  function: func,
                  arg: argument.toString().length,
                  duration: time,
                  port: portname,
                  output: JSON.stringify(answer.result),
                  plugs: JSON.stringify(_plugs)
                })
              }, (error: any) => {
                console.log('runBlock ERROR', error)
                this.$emit('runblock.error', {
                  type: 'error',
                  block: block,
                  call: call,
                  port: portname,
                  function: func,
                  error: error.toString()
                })
              })
            } else {
              call = 'import json\n' + call;
              // If not containerized then run this code
              (window as any).pyodide.runPython(includes)
              const result = (window as any).pyodide.runPythonAsync(code + '\n' + call)

              result.then((res: any) => {
                let answer = res
                var end = Moment(new Date())
                const diff = end.diff(start)
                var time = Moment.utc(diff).format('HH:mm:ss.SSS')

                console.log('CODE CALL RESULT', res)
                // let _result = {}
                if (res === Object(res)) {
                  answer = Object.fromEntries(res.toJs())
                //  _plugs = toObject(answer.plugs)
                //  _result = toObject(answer.result)
                }

                let _result = toObject(answer)
                let _plugs = {}
                if (answer.hasOwnProperty('plugs')) {
                  _plugs = toObject(answer.plugs)
                  _result = toObject(answer.result)
                  console.log('CODE CALL PLUGS', _plugs)
                }
                console.log('CODE CALL ANSWER', answer, _plugs, _result, JSON.stringify(answer))

                this.$emit('message.received', {
                  type: 'result',
                  id: this.id,
                  function: func,
                  port: portname,
                  arg: argument.toString(),
                  duration: time,
                  output: JSON.stringify(_result),
                  plugs: JSON.stringify(_plugs)
                })

                this.$emit('call.completed', {
                  type: 'result',
                  id: this.id,
                  function: func,
                  port: portname,
                  finished: new Date(),
                  arg: argument.toString(),
                  duration: time,
                  output: JSON.stringify(_result),
                  plugs: JSON.stringify(_plugs)
                })
              }, (error: any) => {
                console.log('PYTHON ERROR', error)
                this.$emit('python.error', {
                  type: 'error',
                  id: me.id,
                  args: argdata,
                  port: portname,
                  function: func,
                  error: error.toString()
                })
              })
            }
          }

          this.$emit('refresh')
          // Check all ports
          // If all ports have port.data assigned, then execute the code, where
          // port.function(data,...) where data is in order with the function arguments
          // and argument === the port.name
          // Add the "code" to a python environment, then append the invocation at the end
          // result = invocation(...)
          // Retrieve the result, convert to JSON
          // and emit to any connected ports on this processor
        })
      },
      async execute (data: any) {
        console.log('Running: ', data)
        // noinspection TypeScriptUnresolvedVariable

        // TODO: No longer need this, plugs returned explicitly from functions needing them
        // const plugs = "plugs = {'output A':{}}\n"
        // data = plugs + '\n' + data
        const result = (window as any).pyodide.runPythonAsync(data)
        return result
      },
      listenMessages () {
        var me = this

        socket.on('global', (data: any) => {
          me.messageReceived(data)
        })
        socket.on('execute', (data: any) => {
          me.execute(data)
        })
      },
      messageReceived (msg: any) {
        this.$emit('message.received', msg)
      },
      messageSend (msg: any) {
        const person = <SocketData>msg
        socket.emit('hello', person)
      }
    }
  })
</script>
