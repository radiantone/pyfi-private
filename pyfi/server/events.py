
import eventlet
import socketio
import uvicorn


sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)


@sio.on('servermsg', namespace='/tasks')
async def message(sid, data):
    print("GOT MESSAGE", data)
    await sio.emit('queue', data,
                   namespace='/tasks')


@sio.on('connect', namespace='/tasks')
async def connect(sid, environ):
    print('connect ', sid)
    # await sio.emit('incoming', {'welcome!': 'bar'},
    #         namespace='/chat')
    sio.enter_room(sid, 'lobby', namespace='/tasks')
    print("Entered lobby")


@sio.event(namespace='/tasks')
def my_message(sid, data):
    print('message ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    #eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    uvicorn.run("pyfi.server.events:app", host="127.0.0.1",
                port=5000, log_level="info")
