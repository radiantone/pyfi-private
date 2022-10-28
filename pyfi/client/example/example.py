import json
import os

from pyfi.client.api import Plug, Processor, Socket
from pyfi.client.user import USER
from pyfi.db.model import AlchemyEncoder

"""
Create some infrastructure
"""

# Log in a user first
print("USER", USER)
# Create a processor
processor = Processor(
    name="proc1",
    beat=True,
    user=USER,
    module="ext.processors.sample",
    branch="main",
    concurrency=6,
    gitrepo=os.environ["GIT_REPO"],
)

processor2 = Processor(
    name="proc2",
    user=USER,
    module="ext.processors.sample",
    hostname="radiant",
    concurrency=6,
    branch="main",
    gitrepo=os.environ["GIT_REPO"],
)

# Create a socket on the processor to receive requests for the do_something python function(task)
do_something = Socket(
    name="ext.processors.sample.do_something",
    user=USER,
    interval=5,
    processor=processor,
    queue={"name": "pyfi.queue1"},
    task="do_something",
)

print(json.dumps(do_something.socket, indent=4, cls=AlchemyEncoder))
# Create a socket on the processor to receive requests for the do_this python function(task)
do_this = Socket(
    name="ext.processors.sample.do_this",
    user=USER,
    processor=processor2,
    queue={"name": "pyfi.queue2"},
    task="do_this",
)

do_something2 = Socket(
    name="proc2.do_something",
    user=USER,
    processor=processor2,
    queue={"name": "pyfi.queue1"},
    task="do_something",
)
# Create a plug that connects one processor to a socket of another
plug = Plug(
    name="plug1",
    processor=processor,
    user=USER,
    source=do_something,
    queue={"name": "pyfi.queue3"},
    target=do_this,
)

# for p in processor.get().processor.plugs:
#    print(p.target.queue)
# Send a message to a socket(function).
# result = do_something("Hello World !")

# print("RESULT",result)
