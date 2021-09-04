from pyfi.client.api import Socket as Function

# Look up a socket function and invoke it
do_something = Function(name='pyfi.processors.sample.do_something')

# Send a message to the socket function
result = do_something("Hello World XXX!")

print("Result is: ",result.get())
