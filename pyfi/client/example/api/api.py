from pyfi.client.api import Socket as Function
from pyfi.client.user import USER

# Grab specific socket by name, we don't know the task
# do_something = Function(name="proc1.do_something", user=USER)
# Grab any socket with this task, we don't know the socket
do_something = Function(module="ext.processors.sample", task="do_something", user=USER)
do_something_p = do_something.p

# do_this = Function(name="proc2.do_this", user=USER)
# Grab any socket with this task, we don't care
do_this = Function(module="ext.processors.sample", task="do_this", user=USER)
do_this_p = do_this.p
