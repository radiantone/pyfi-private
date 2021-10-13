from pyfi.client.api import Socket as Function
from pyfi.client.user import USER

do_something = Function(name='pyfi.processors.sample.do_something', user=USER)
do_something_p = do_something.p

do_this = Function(name='pyfi.processors.sample.do_this', user=USER)
do_this_p = do_this.p
