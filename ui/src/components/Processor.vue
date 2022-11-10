
<script lang="ts">
/* eslint-disable @typescript-eslint/no-unsafe-assignment,@typescript-eslint/no-unsafe-call */
import { Wrapper } from '../util'
import Vue from 'vue'
import mixins from 'vue-typed-mixins'
import { io, Socket } from 'socket.io-client'
// import { loadPyodide } from "pyodide"
// eslint-disable-next-line @typescript-eslint/no-var-requires
// import { loadPyodide } from "pyodide"
// const { loadPyodide } = require('pyodide')

// const pyodide = loadPyodide()

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
}

export const ProcessorMixin = Vue.extend({
  data () {
    return {
      name: 'Processor',
      portobjects: {},
      argobjects: {}
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

export default mixins(ProcessorBase).extend<ProcessorState,
  Methods,
  Computed,
  Props>({
    data () {
      return {
        name: 'MyProcessor',
        id: 'any',
        portobjects: {},
        argobjects: {}
      }
    },

    created () {
      var me = this

      socket.on('basicEmit', (a, b, c) => {
        me.$store.commit('designer/setMessage', b)
      })
      me.listenMessages()
    },
    computed: {
    /*
    connected() {
      return this.$store.state.designer.connected;
    },
    streaming() {
      return this.$store.state.designer.streaming;
    }, */
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
        (window as any).root.$on(id, async (code: string, func: string, argument: string, data: any) => {
          let obj = data
          this.id = id
          if (data === Object(data)) {
            obj = Object.fromEntries(data.toJs())
          }

          console.log('NODE DATA RECEIVED', id, func, argument, obj)

          let port = null
          for (var i = 0; i < this.portobjects[func].length; i++) {
            if (this.portobjects[func][i].name === argument) {
              port = this.portobjects[func][i]
              port.data = obj
            }
          }
          console.log('PROCESSOR EXECUTING PORT', func, argument, data, port)

          let complete = true
          for (var i = 0; i < this.portobjects[func].length; i++) {
            const port = this.portobjects[func][i]
            if (port.data === undefined) {
              complete = false
              break
            }
          }
          if (complete) {
            console.log('FUNCTION', func, 'IS COMPLETE!')
            console.log('   INVOKING:', func)
            let call = func + '('
            let count = 0
            this.portobjects[func].forEach((_arg: any) => {
              const jsonarg = JSON.stringify(_arg.data)
              console.log('    ARG:', _arg, jsonarg)
              if (count > 0) {
                call = call + ','
              }
              call = call + jsonarg
              count += 1
            })
            call = call + ')'
            console.log('FUNCTION CALL', call)
            console.log('CODE CALL', code + '\n' + call)
            const result = (window as any).pyodide.runPythonAsync(code + '\n' + call)

            result.then((res: any) => {
              let answer = res

              if (res === Object(res)) {
                answer = Object.fromEntries(res.toJs())
              }
              console.log('CODE CALL RESULT', answer)
              this.$emit('message.received', {
                'type': 'result',
                'id': this.id,
                'function': func,
                'output': JSON.stringify(answer)
              })
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

interface MessageListener {
  messageReceived(message: any): void;

  messageSend(message: any): void;
  getPort(func: string, name: string): any;
  listenMessages(): void;
  setId(id: string): void;
  execute(data: any): void;
}

type Methods = MessageListener

interface Computed {
}

interface Props {
  wrapper: Wrapper;
}
</script>
