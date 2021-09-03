from pyfi.client.api import Socket as Function

# Look up a socket and invoke it
do_something = Function(name='pyfi.processors.sample.do_something')

# Send a message to the socket
do_something("Hello World XXX!")
