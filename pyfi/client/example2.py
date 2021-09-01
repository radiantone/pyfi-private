from pyfi.client.api import Socket

# Look up a socket and invoke it
do_something = Socket(name='proc1.socket1')

# Send a message to the socket
do_something("Hello World XXX!")
