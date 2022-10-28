from pyfi.client.api import Task

# Create a socket on the processor to receive requests for the do_something python function(task)
do_something = Task(
    name="do_something",
    module="ext.processors.sample",
    queue={"name": "sockq1.topic", "type": "fanout"},
)

# Send a message to all task sockets listening on pyfi.queue1
result = do_something("Hello World !")

print("RESULT", result.get())
