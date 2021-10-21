import os
import json
import configparser

from pathlib import Path
from pyfi.client.api import Processor, Socket, Plug
from pyfi.db.model import AlchemyEncoder
from pyfi.config import CONFIG
from pyfi.client.user import USER

# Log in a user first
print("USER", USER)
# Create a socket on the processor to receive requests for the do_something python function(task)
do_something = Socket(name='pyfi.processors.sample.do_something', user=USER, interval=30, queue={'name': 'pyfi.queue1.topic'}, task='do_something')

# Send a message to a socket(function).
result = do_something("Hello World !")

print("RESULT",result)
