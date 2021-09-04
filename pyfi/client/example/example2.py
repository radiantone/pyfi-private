from pyfi.client.example.api import do_something

# Send a message to the socket function
result = do_something("Inner "+" ".join(do_something("Hello World XXX!")))

print("Result is: ",result)
