"""
Decorator API for PYFI/Flow. Defines network from plain old classes and methods.
"""
import os

from pyfi.client.api import ProcessorBase
from pyfi.client.decorators import agent, network, node, plug, processor, socket


@network(name="network-1")
@node(name="node2", hostname="agent2")
@agent(name="ag2")
@processor(
    name="proc2",
    deployment="proc2.deploy",
    gitrepo=os.environ["GIT_REPO"],
    module="ext.processors.sample",
    concurrency=6,
)
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
@node(name="node1", hostname="phoenix")
@agent(name="ag1")
@processor(
    name="proc1",
    deployment="proc1.deploy",
    gitrepo=os.environ["GIT_REPO"],
    module="ext.processors.sample",
)  # gitrepo and module can be implied
class ProcessorA(ProcessorBase):
    """Description"""

    def get_message(self):
        return "Self message!"

    @plug(
        name="plug1",
        target="sock2",  # Must be defined above already (prevents cycles)
        queue={
            "name": "queue1",
            "message_ttl": 300000,
            "durable": True,
            "expires": 200,
        },
    )
    @socket(
        name="sock1", processor="proc1", beat=True, interval=5, queue={"name": "sockq1"}
    )
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


if __name__ == "__main__":
    print("Network created.")
