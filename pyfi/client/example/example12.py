"""
This is the decorator API for PYFI. To build infrastructure you layer decorators with keyword arguments to configure them

The @node decorator will create a node for the given "hostname". Lower layer decorators such as @agent, @worker, @processor
can then be used and passed keyword args to configure them. Some decorators are optional and defaults will be used.

At the class level if the @processor decorator which will use the current python module for the processor and each method in
the class becomes a "task" of the processor. The type of task is "class" and the classname is stored on the class.
Moreover the code of the task is stored on the task object and used for executing the task.

The processor still provides a gitrepo or container image to be used to run the code. It is assumed that the code dependencies
for the task methods are provided by the container or gitrepo.
"""
from pyfi.client.user import USER
from pyfi.client.api import parallel, pipeline
from pyfi.client.api import Socket
from pyfi.client.api import network, node, agent, processor, worker, socket, plug

"""
Declare an infrastructure node in the database that can be immediately used.
"""
@network(name="network-1")
@node(name="node1", hostname="agent2")
@agent(name="ag2")
@processor(name="proc2", gitrepo="", module="pyfi.processors.sample", concurrency=6)
class ProcessorB:
    """Description"""

    # socket can also be implied
    @socket(name="sock2", processor="proc2", queue={"name": "sockq2"})
    def do_this(message):
        from random import randrange

        print("Do this!", message)
        message = "Do this String: " + str(message)
        graph = {
            "tag": {"name": "tagname", "value": "tagvalue"},
            "name": "distance",
            "value": randrange(50),
        }
        return {"message": message, "graph": graph}

@network(name="network-1")
@node(name="node1", hostname="agent2")
@agent(name="ag2")
@processor(name="proc1", gitrepo="", module="pyfi.processors.sample")  # gitrepo and module can be implied
class ProcessorA:
    """Description"""

    @plug(
        name="plug1",
        target="sock2",
        queue={
            "name": "queue1",
            "message_ttl": 300000,
            "durable": True,
            "expires": 200,
        },
    )
    @socket(name="sock1", processor="proc1", queue={"name": "sockq1"})
    def do_something(message):
        """do_something"""
        from random import randrange

        message = "TEXT:" + str(message)
        graph = {
            "tag": {"name": "tagname", "value": "tagvalue"},
            "name": "temperature",
            "value": randrange(10),
        }
        return {"message": message, "graph": graph}


# Processors can be defined without nodes or agents. A scheduler will place
# any processors without nodes or agents. In the example below we are placing
# the processor on agent "ag2"
#@agent(name="ag2")  



do_something = Socket(name="sock1", user=USER).p

'''
_pipeline = pipeline(
    [
        do_something("One"),
        do_something("Two"),
        parallel(
            [
                do_something("Four"),
                do_something("Five"),
            ]
        ),
        do_something("Three"),
    ]
)
'''