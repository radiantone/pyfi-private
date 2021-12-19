from pyfi.client.api import Socket
from pyfi.client.user import USER

# do_something = Socket(name='pyfi.processors.sample.do_something', user=USER)
do_something = Socket(name='pyfi.processors.sample.do_something', loadbalanced=True, user=USER)

result = do_something("Example 3 result!")

print("RESULT", result)

# do_this = Socket(name='pyfi.processors.sample.do_this')

# result = do_this("Another result!")

# print("RESULT", result)
