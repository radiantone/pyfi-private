from pyfi.client.api import Socket
from pyfi.client.user import USER

# do_something = Socket(name='pyfi.processors.sample.do_something', user=USER)
emit_one = Socket(name="pyfi.processors.sample.emit_one", loadbalanced=True, user=USER)

result = emit_one(10)

print("RESULT", result)
