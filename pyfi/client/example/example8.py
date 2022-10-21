from pyfi.client.api import parallel
from pyfi.client.example.api import do_something_p as do_something

_fork = parallel(
    [
        do_something("Four"),
        do_something("Five"),
    ]
)

result = _fork().get()
print("RESULT:", result)

"""
# fork takes the head (first arg), executes it and passes the result to the body (second arg) running each in parallel
_pipeline = pipeline(
    do_something("One"),
    do_something("Two"),
    do_something("Three"),
    fork(parallel([
        do_something("Four"),
        do_something("Five"),
    ])))

result = _pipeline().get()
print("RESULT:",result)

class f:

    def __init__(self, val):
        self.val = val

    def __or__(self, other):
        print("OR! ", self.val, other.val)
        return f(str(self.val) + other.val)

_f = f('F')
_a = f('A')

_f | _a | _f

from functools import reduce
import operator

reduce(operator.or_, [_fork, _fork], _fork)

_f | fork([
    do_this,
    do_this,
    do_this
])
"""
