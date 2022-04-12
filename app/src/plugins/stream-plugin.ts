import Vue from "vue";
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


export default {
  // called by Vue.use(FirstPlugin)
  install(Vue : any, options : any) {
    // create a mixin

    const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io(
      'http://localhost'
    );
    socket.on("basicEmit", (a, b, c) => {
      console.log("STREAM PLUGIN: SERVER EMIT", a, b, c)
    });
    Vue.mixin({
      created() {
        //console.log("FIRST PLUGIN",Vue);
      },
    });
  },
};