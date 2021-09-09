""" Example"""
from pyfi.client.api import parallel, pipeline, funnel
from pyfi.client.example.api import do_something_p as do_something

_pipeline = pipeline([
    do_something("One"),
    do_something("Two"),
    do_something("Three")])

_funnel = funnel([
    do_something("A")])

print("FUNNEL: ", _funnel(_pipeline).get())
