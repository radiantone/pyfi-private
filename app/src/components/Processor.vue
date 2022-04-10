<script lang="ts">

import { Wrapper } from '../util';
import Vue from 'vue';
import mixins from 'vue-typed-mixins';
import { io, Socket } from 'socket.io-client';

interface ServerToClientEvents {
  noArg: () => void;
  basicEmit: (a: number, b: string, c: Buffer) => void;
  withAck: (d: string, callback: (e: number) => void) => void;
}

interface ClientToServerEvents {
  hello: (data: SocketData) => void;
}

interface SocketData {
  name: string;
  age: number;
}

const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(
  'http://localhost'
);
socket.on("basicEmit", (a, b, c) => {
  console.log("SERVER EMIT",a,b,c)
});
export interface ProcessorState {
    name: string;
}

export const ProcessorMixin = Vue.extend({
   data() {
       return {
           name:"Processor"
       }
   }
});

export class ProcessorBase extends ProcessorMixin implements ProcessorState {
    name!: ProcessorState['name'];
}

export default mixins(ProcessorBase).extend<ProcessorState,
  Methods,
  Computed,
  Props>({
  data() {
    return {
        name:"MyProcessor"
    };
  },
  created() {
  },
  computed: {
   
  },
  mounted() {
  },
  methods: {
    messageReceived(msg) {

    },
    messageSend(msg) {
        const person = <SocketData>msg;
        socket.emit('hello', person);
    }
  },
});

interface MessageListener {
  messageReceived(message: any): void;
  messageSend(message: any): void;
}

interface Methods extends MessageListener {
}

interface Computed {

}

interface Props {
  wrapper: Wrapper;
}
</script>