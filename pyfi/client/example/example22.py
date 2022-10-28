"""
Decorator API for PYFI/Flow. Defines network from plain old classes and methods.
"""
import os

from pyfi.client.api import ProcessorBase
from pyfi.client.decorators import processor, socket


@processor(
    name="proc1",
    gitrepo=os.environ["GIT_REPO"],
    module="ext.processors.sample",
    concurrency=6,
)
class ProcessorA(ProcessorBase):
    """Description"""

    def get_message(self):
        return "Self message!"

    @socket(
        name="proc1.do_something",
        processor="proc1",
        beat=False,
        interval=15,
        queue={"name": "sockq1"},
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
