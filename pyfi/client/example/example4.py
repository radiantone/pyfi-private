""" Example"""
from pyfi.client.api import parallel, pipeline, funnel
from pyfi.client.example.api import do_something_p as do_something

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
    do_something("Nine")])

print("FUNNEL: ", _funnel(do_something("Four")).get())
