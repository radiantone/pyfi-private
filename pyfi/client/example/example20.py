"""
Decorator API for PYFI/Flow. Defines network from plain old classes and methods.
"""
import os
from pyfi.client.api import ProcessorBase, network, node, agent, worker, processor, socket, plug
from pyfi.client.user import USER
from pyfi.client.api import Registry, Node, Agent, Worker, Processor, Socket, Plug, Task, Network, Deployment


@processor(name="proc2", gitrepo=os.environ['GIT_REPO'], module="pyfi.processors.sample", concurrency=3)
class ProcessorB(ProcessorBase):
    """Description"""

    @socket(name="pyfi.processors.sample.do_this", processor="proc2", arguments=True, queue={"name": "sockq2"})
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


@processor(name="proc1", gitrepo=os.environ['GIT_REPO'], id='proc1id', module="pyfi.processors.sample", concurrency=6)
class ProcessorA(ProcessorBase):
    """Description"""

    def get_message(self):
        return "Self message!"

    @plug(
        name="plug1",
        target="pyfi.processors.sample.do_this",  # Must be defined above already (prevents cycles)
        queue={
            "name": "queue1",
            "message_ttl": 300000,
            "durable": True,
            "expires": 200,
        }
    )
    @socket(name="pyfi.processors.sample.do_something", processor="proc1", beat=True, interval=5, queue={"name": "sockq1"})
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


if __name__ == '__main__':
    network = Network(name='network-1', user=USER)
    node2 = Node(name='node2',hostname='agent2')
    node3 = Node(name='node3',hostname='agent3')
    network.nodes += [node2,node3]

    agent2 = Agent(name='agent2',hostname='agent2')
    node2.agent = agent2

    agent3 = Agent(name='agent3',hostname='agent3')
    node3.agent = agent3

    worker2 = Worker(name='worker2',hostname='agent2')
    agent2.worker = worker2
    worker3 = Worker(name='worker3',hostname='agent3')
    agent3.worker = worker3

    deployment = Deployment(
            hostname='agent2', name='agent2.deploy.proc1', processor_id='proc1id', cpus=2
        )
    print("Network created.")