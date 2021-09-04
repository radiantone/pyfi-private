from pyfi.client.example.api import do_something
from celery import chord

# Send a message to the socket function
result = do_something("Inner "+" ".join(do_something("Hello World XXX!")))

print("Result is: ",result)

counting = chord([
    do_something.p("One"), 
    do_something.p("Two"), 
    do_something.p("Three") ])


print("COUNTING: ", counting())
