"""

"""
from pyfi.client.user import USER
from pyfi.client.api import parallel, pipeline
from pyfi.client.api import ProcessorBase, network, node, agent, processor, worker, socket, plug

@network(name="network-1")
@node(name="node1", hostname="agent2")
@agent(name="ag2")
@processor(name="proc2", deploy=True, gitrepo="https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor", module="pyfi.processors.sample", concurrency=6)
class ProcessorB(ProcessorBase):
    """Description"""

    @socket(name="sock2", processor="proc2", arguments=True, queue={"name": "sockq2"})
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
@node(name="node2", hostname="phoenix")
@agent(name="ag2")
@processor(name="proc1", deploy=True, gitrepo="https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor", module="pyfi.processors.sample")  # gitrepo and module can be implied
class ProcessorA(ProcessorBase):
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


proca = ProcessorA()
# Synchronous method call
print("Hi!",proca.do_something("HI!"))

# Get parallel method handle
do_something = proca.do_something.p

# Asynchronous workflow
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

# Wait for result and print it
print(_pipeline().get())
