"""
Decorator API for PYFI/Flow. Defines network from plain old classes and methods.
"""
from pyfi.client.api import ProcessorBase, network, node, agent, processor, socket, plug


@processor(name="proc2", requested_status="deploy", gitrepo="https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor", module="pyfi.processors.sample", concurrency=6)
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


@processor(name="proc1", requested_status="deploy",gitrepo="https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor", module="pyfi.processors.sample")  # gitrepo and module can be implied
class ProcessorA(ProcessorBase):
    """Description"""

    def get_message(self):
        return "Self message!"

    @plug(
        name="plug1",
        target="sock2",     # Must be defined above already (prevents cycles)
        queue={
            "name": "queue1",
            "message_ttl": 300000,
            "durable": True,
            "expires": 200,
        }
    )
    @socket(name="pyfi.processors.sample.do_something'", processor="proc1", beat=True, interval=5, queue={"name": "sockq1"})
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
    print("Network created.")