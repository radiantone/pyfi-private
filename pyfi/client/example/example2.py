from os import pipe
from pyfi.client.example.api import do_something, parallel, pipeline

# Send a message to the socket function
result = do_something("Inner "+do_something("Hello World XXX!"))

print("Result is: ",result)

result = pipeline([
    do_something.p("One"), 
    do_something.p("Two"), 
    do_something.p("Two")])()

def callback(*args, **kwargs):
    return

print("COUNTING: ", result.get())
