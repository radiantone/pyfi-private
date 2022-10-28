from pyfi.client.api import Socket
from pyfi.client.user import USER

do_something = Socket(name="ext.processors.sample.do_something", user=USER)

result = do_something("Example 3 result!")

print("RESULT", result)

do_this = Socket(name="ext.processors.sample.do_this", user=USER)

while True:
    result = do_something("Another result!")
    print("RESULT", result)
