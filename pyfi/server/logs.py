import os

import uvicorn
from redis import Redis

r = Redis(host=os.environ["REDIS_SERVER"], port=6379, db=0)


class App:
    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )
        await send({"type": "http.response.body", "body": b"Hello, world!"})


def event_handler(msg):
    print("Handler", msg)
    # parse to JSON
    # Push to elastic search


if __name__ == "__main__":
    # eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    pubsub = r.pubsub()

    pubsub.psubscribe(**{"celery-task*": event_handler})

    pubsub.run_in_thread(sleep_time=0.01)
    uvicorn.run(
        "pyfi.server.redispush:App", host="127.0.0.1", port=5001, log_level="info"
    )
