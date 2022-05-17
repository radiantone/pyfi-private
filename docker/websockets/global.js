const io = require("socket.io-client");


const socket = io("ws://localhost:3003");

socket.on("proc1", (...args) => {
    console.log("proc1:", args);
});
socket.on("proc2", (...args) => {
    console.log("proc2:", args);
});
