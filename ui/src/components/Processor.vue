<script lang="ts">
/* eslint-disable @typescript-eslint/no-unsafe-assignment,@typescript-eslint/no-unsafe-call */
import Vue from 'vue'
import mixins from 'vue-typed-mixins'
import { Wrapper } from '../util'
import { io, Socket } from 'socket.io-client'
import { parseCronExpression, IntervalBasedCronScheduler } from 'cron-schedule'
import Moment from 'moment/moment'
const scheduler = new IntervalBasedCronScheduler(1000)

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
  portobjects: { [key: string]: any };
  argobjects: { [key: string]: any };
  errorobjects: { [key: string]: any };
}

export const ProcessorMixin = Vue.extend({
  data () {
    return {
      name: 'Processor',
      portobjects: {},
      argobjects: {},
      errorobjects: {}
    }
  }
})

export class ProcessorBase extends ProcessorMixin implements ProcessorState {
  name!: ProcessorState['name'];
  id!: ProcessorState['id'];
}

const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(
  'http://localhost'
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
}

type Methods = ProcessorInterface

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
        name: 'MyProcessor',
        id: 'any',
        portobjects: {},
        argobjects: {},
        errorobjects: {}
      }
    },

    created () {
      var me = this

      socket.on('basicEmit', (a, b, c) => {
        me.$store.commit('designer/setMessage', b)
      })
      me.listenMessages()
    },
    watch: {
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
    methods: {
      getVersion () {
        if (this.$store.state.designer.version.indexOf('Free') >= 0) {
          return 'FREE'
        } else {
          return 'DEV'
        }
      },
      startSchedule (cronstr: string) {
        var me = this
        console.log('UPDATING CRON')
        scheduler.stop()
        const cron = parseCronExpression(cronstr)
        scheduler.registerTask(cron, () => {
          console.log(new Date(), this.name, 'TASK EXECUTED')
          me.$emit('message.received', {
            type: 'trigger'
          })
        })
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

        (window as any).root.$on(id, async (code: string, func: string, argument: string, data: any) => {
          let obj = data
          this.id = id
          if (data instanceof Map) {
            obj = mapToObj(<Map<string, any>>data)
          } else if (data instanceof Object) {
            obj = Object.fromEntries(data.toJs())
          }

          console.log('NODE DATA RECEIVED', id, func, argument, obj)

          let port = null
          for (var i = 0; i < me.portobjects[func].length; i++) {
            if (me.portobjects[func][i].name === argument) {
              port = me.portobjects[func][i]
              port.data = obj
            }
          }
          console.log('PROCESSOR EXECUTING PORT', func, argument, data, port)

          let complete = true
          for (var i = 0; i < me.portobjects[func].length; i++) {
            const port = me.portobjects[func][i]
            if (port.data === undefined) {
              complete = false
              break
            }
          }
          if (complete) {
            debugger
            console.log('FUNCTION', func, 'IS COMPLETE!')
            console.log('   INVOKING:', func)
            const plugs = "plugs = {'output A':{}}\n"
            let call = func + '('
            let count = 0
            me.portobjects[func].forEach((_arg: any) => {
              let jsonarg

              // If we already have JSON encoded data, then pass it along
              // otherwise, convert it to JSON
              let isobj = false
              if (_arg.data instanceof Object) {
                isobj = true
                try {
                  JSON.parse(_arg.data)
                  jsonarg = _arg.data
                } catch (err) {
                  if (_arg.data instanceof Object) {
                    jsonarg = JSON.stringify(_arg.data)
                  } else {
                    jsonarg = _arg.data
                  }
                }
              } else {
                jsonarg = _arg.data
              }
              debugger
              console.log('    ARG:', _arg, jsonarg)
              if (count > 0) {
                call = call + ','
              }

              // We have to double encode and decode the data because the raw
              // json output is not python object compatible. So we have to convert the raw
              // JSON result to a JSON string which can then be converted to a python object
              // with json.loads
              if (isobj) {
                call = call + 'json.loads(' + JSON.stringify(jsonarg) + ')'
              } else {
                call = call + jsonarg
              }
              count += 1
            })
            call = call + ')'
            call = plugs + '\n' + 'import json\n' + call
            console.log('FUNCTION CALL', call)
            console.log('CODE CALL', code + '\n' + call)
            var start = Moment(new Date())
            const result = (window as any).pyodide.runPythonAsync(code + '\n' + call)

            result.then((res: any) => {
              const _plugs = (window as any).pyodide.globals.get('plugs').toJs()
              let answer = res
              var end = Moment(new Date())
              const diff = end.diff(start)
              var time = Moment.utc(diff).format('HH:mm:ss.SSS')
              if (res === Object(res)) {
                answer = Object.fromEntries(res.toJs())
              }
              console.log('CODE CALL RESULT', answer)
              this.$emit('message.received', {
                type: 'result',
                id: this.id,
                function: func,
                duration: time,
                output: JSON.stringify(answer)
              })
            }, (error: any) => {
              debugger
              console.log('PYTHON ERROR')
            })
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
        const plugs = "plugs = {'output A':{}}\n"
        data = plugs + '\n' + data
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
