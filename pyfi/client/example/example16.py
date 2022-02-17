"""
Create subclass of HTTPProcessor
"""
from pyfi.client.library import HTTPProcessor
from pyfi.client.api import network, node, agent, processor, socket, plug


@network(name="network-1")
@node(name="node3", hostname="agent2")
@agent(name="ag3")
@processor(name="http_proc", deployment="http_proc.deploy", module="pyfi.processors.sample", concurrency=6)
class MyHTTPProcessor(HTTPProcessor):

    @socket(name="sock2", processor="http_proc", arguments=True, queue={"name": "sockq2"})
    def http_get(self, *args, **kwargs):
        super(MyHTTPProcessor, self).http_get(*args, **kwargs)
