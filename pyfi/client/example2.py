from pyfi.client.api import Socket as Function

# Look up a socket function and invoke it
do_something = Function(name='pyfi.processors.sample.do_something')

# Send a message to the socket function
do_something("Hello World XXX!")
