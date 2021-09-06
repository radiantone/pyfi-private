from pyfi.client.api import Socket as Function

do_something = Function(name='pyfi.processors.sample.do_something')
do_something_p = do_something.p

do_this = Function(name='pyfi.processors.sample.do_this')
do_this_p = do_this.p
