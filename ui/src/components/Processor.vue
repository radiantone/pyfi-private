
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
}

export const ProcessorMixin = Vue.extend({
  data () {
    return {
      name: 'Processor'
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
        id: 'any'
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
      setId (id: string) {
        (window as any).root.$on(id, (code: string, func: string, argument: string, data: any) => {
          console.log('NODE DATA RECEIVED', id, code, func, argument, data)

          // Store data with func and argument
          // Check func if all stored arguments are present, if so, then invoke it
          // regex find func"name" in code and named args order
          // retrieve stored args by name and put in same order
          // construct function call string and add to end of code, execute
          // get result

          // emit result to all port/edges
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
