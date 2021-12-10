""" Example"""
from pyfi.client.api import parallel, pipeline, funnel
from pyfi.client.example.api import do_something_p as do_something

'''
An example app on top of pyfi. References existing infrastructure and then runs complex workflows and parallel operations on it
'''
_pipeline = pipeline([
    do_something("One"),
    do_something("Two"),
    parallel([
        do_something("Four"),
        do_something("Five"),
    ]),
    do_something("Three")])

_parallel = parallel([
    _pipeline,
    do_something("Six"),
    do_something("Seven")])

_funnel = funnel([
    do_something("Eight"),
    _parallel,
    do_something("Nine")], do_something("A"))

_funnel2 = funnel([
    _parallel,
    do_something("Ten")],do_something("B"))

_funnel3 = funnel([
    _funnel,
    _funnel2])

result = _funnel3(do_something("Eleven"))
print("FUNNEL: ", result.get())
