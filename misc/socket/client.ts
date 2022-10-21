import { io, Socket } from "socket.io-client";
interface ServerToClientEvents {
  noArg: () => void;
  basicEmit: (a: number, b: string, c: Buffer) => void;
  global: (data: any) => void;
  withAck: (d: string, callback: (e: number) => void) => void;
}

interface ClientToServerEvents {
  hello: (data: SocketData) => void;
}
interface SocketData {
  name: string;
  age: number;
}
const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io("http://localhost:3003");
socket.emit("hello",{name:"Darren",age:51});
