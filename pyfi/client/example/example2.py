from pyfi.client.example.api import do_something
from celery import group,chain

# Send a message to the socket function
result = do_something("Inner "+" ".join(do_something("Hello World XXX!")))

print("Result is: ",result)
result = group([
    do_something.p("One"), 
    do_something.p("Two"), 
    do_something.p("Two")])()

def callback(*args, **kwargs):
    return

print("COUNTING: ", result.get())
