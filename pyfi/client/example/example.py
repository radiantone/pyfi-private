import os
import json
import configparser

from pathlib import Path
from pyfi.client.api import Processor, Socket, Plug
from pyfi.db.model import AlchemyEncoder
from pyfi.config import CONFIG
from pyfi.client.user import USER

# Log in a user first
print("USER",USER)
# Create a processor
processor = Processor(name='proc1', beat=True, user=USER, module='pyfi.processors.sample', branch='main', concurrency=6,
                      gitrepo='https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor')

processor2 = Processor(name='proc2', user=USER, module='pyfi.processors.sample', hostname='agent1', concurrency=6, branch='main',
                       gitrepo='https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor')


# Create a socket on the processor to receive requests for the do_something python function(task)
do_something = Socket(name='proc1.do_something', user=USER, interval=30,
                      processor=processor, queue={'name': 'pyfi.queue1', 'expires':300, 'durable':True, 'message_ttl':30000}, task='do_something')
print(json.dumps(do_something.socket, indent=4, cls=AlchemyEncoder))
# Create a socket on the processor to receive requests for the do_this python function(task)
do_this = Socket(name='proc2.do_this', user=USER,
                 processor=processor2, queue={'name': 'pyfi.queue2', 'expires': 300, 'durable': True, 'message_ttl': 30000}, task='do_this')

do_something2 = Socket(name='proc2.do_something', user=USER, processor=processor2, queue={'name': 'pyfi.queue2'}, task='do_something')
# Create a plug that connects one processor to a socket of another
plug = Plug(name='plug1', processor=processor, user=USER,
            source=do_something, queue={'name': 'pyfi.queue2'}, target=do_this)

# Send a message to a socket(function). 
#result = do_something("Hello World !")

#print("RESULT",result)
