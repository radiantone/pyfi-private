from pyfi.client.api import Processor, Socket

# Create a processor
processor = Processor(name='proc1', module='pyfi.processors.sample', branch='main',
                      gitrepo='https://github.com/radiantone/pyfi-processors')

# Create a socket for that processor
do_something = Socket(name='proc1.socket1', processor=processor, queue={
                'name': 'pyfi.queue1'}, task='do_something')

do_this = Socket(name='proc1.socket2', processor=processor, queue={
    'name': 'pyfi.queue1'}, task='do_this')

# Send a message to a socket
do_something("Hello World !")

do_this("Do this!!")

