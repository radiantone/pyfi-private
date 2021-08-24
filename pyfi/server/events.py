
import socketio
import uvicorn
import json

sio = socketio.AsyncServer(async_mode='asgi')
app = socketio.ASGIApp(sio)

'''
Workers will send messages to specific rooms such as pyfi.queue1.proc1 with messages
for that processor name. invoke pyfi listen pyfi.queue1.proc1 --namespace tasks will listen
to messages on that channel.

processor socket tasks (functions) can post messages to the room which can be spotted by
pyfi components such as logs, charts and graphs for real-time visualization
'''


@sio.on('servermsg', namespace='/tasks')
async def server_message(sid, data):
    print("GOT MESSAGE", data)
    await sio.emit('queue', data,
                   namespace='/tasks')

    #await sio.emit('task', data, room='pyfi.queue1.proc1',  namespace='/tasks')
    #print("Sent to task")

@sio.on('roomsg', namespace='/tasks')
async def room_message(sid, data):
    print("ROOM MESSAGE", data)
    #await sio.emit(_data['channel'], _data['message'], skip_sid=sid)
    await sio.emit(data['channel'], data['message'], room=data['room'],  namespace='/tasks')

@sio.on('connect', namespace='/tasks')
async def connect(sid, environ):
    print('connect ', sid)
    # await sio.emit('incoming', {'welcome!': 'bar'},
    #         namespace='/chat')
    sio.enter_room(sid, 'lobby', namespace='/tasks')
    print("Entered lobby")


@sio.on('join', namespace='/tasks')
async def on_join(sid, data):
    channel = data['room']
    print("Entering room", channel)
    sio.enter_room(sid, channel, namespace='/tasks')


@sio.event
async def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    uvicorn.run("pyfi.server.events:app", host="0.0.0.0",
                port=5000, log_level="info")
