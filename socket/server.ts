import { createServer } from "http";
import { Server, Socket, ServerOptions } from "socket.io";

const httpServer = createServer();

interface ServerToClientEvents {
  noArg: () => void;
  basicEmit: (a: number, b: string, c: Buffer) => void;
  withAck: (d: string, callback: (e: number) => void) => void;
}

interface ClientToServerEvents {
  hello: (data: SocketData) => void;
}

interface InterServerEvents {
  ping: () => void;
}

interface SocketData {
  name: string;
  age: number;
}

const options: Partial<ServerOptions> = {
  cors: {
    origin: "*"
  }
}

const io = new Server<ClientToServerEvents, ServerToClientEvents, InterServerEvents, SocketData>(httpServer, options);

io.on("connection", (socket) => {
  console.log("Cient connected",socket);
  socket.on("hello", (data: SocketData) => {
    console.log("CLIENT SAYS HELLO!", data);
  setTimeout( () => {
      io.to("processorA").emit("basicEmit", 1, "Linking...", Buffer.from([3]));
  },3000);
  });
  socket.emit("noArg");
  //socket.emit("basicEmit", 1, "Linking...", Buffer.from([3]));
  socket.emit("withAck", "4", (e) => {
    // e is inferred as number
  });
  socket.join("processorA");

  // and then later
  setTimeout( () => {
      io.to("processorA").emit("basicEmit", 1, "Linking...", Buffer.from([3]));
  },3000);

  // works when broadcast to all
  io.emit("noArg");

});


console.log("Listening on 3003...");
httpServer.listen(3003);
