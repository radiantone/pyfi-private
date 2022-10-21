""" Example"""

from pyfi.client.api import parallel
from pyfi.client.example.api import do_something_p as do_something

"""
An example app on top of pyfi. References existing infrastructure and then runs complex workflows and parallel operations on it
"""
_pipeline = parallel(
    [
        do_something("One"),
        do_something("Two"),
        do_something("Three"),
    ]
)
print(_pipeline().get())
_pipeline2 = parallel(
    [
        do_something("One"),
        _pipeline,
        do_something("Three"),
    ]
)

print("pipeline")
print(_pipeline().get())
print("pipeline2")
print(_pipeline2().get())
