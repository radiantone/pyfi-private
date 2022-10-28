from pyfi.client.api import Socket
from pyfi.client.user import USER

# do_something = Socket(name='sock1', loadbalanced=True, user=USER)
do_something = Socket(
    name="ext.processors.sample.do_something", loadbalanced=True, user=USER
)
# emit_one = Socket(name="ext.processors.sample.emit_one", loadbalanced=True, user=USER)

# result = emit_one(10)
result = do_something("HI!!!")
print("RESULT", result)
