import configparser
import json
import os
from pathlib import Path

from pyfi.client.api import Task
from pyfi.client.user import USER
from pyfi.config import CONFIG
from pyfi.db.model import AlchemyEncoder

# Log in a user first
print("USER", USER)
# Create a socket on the processor to receive requests for the do_something python function(task)
do_something = Task(
    name="do_something",
    module="pyfi.processors.sample",
    queue={"name": "pyfi.queue1.topic", "type": "fanout"},
)

# Send a message to all task sockets listening on pyfi.queue1
result = do_something("Hello World !")

print("RESULT", result)
