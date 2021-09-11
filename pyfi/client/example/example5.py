""" Example"""
from pyfi.client.api import parallel, pipeline, fork, funnel

# Function API over your processor models
# do_something is my python function mounted onto a processor from my github repo
from pyfi.client.example.api import do_something_p as do_something, do_this_p as do_this

# Durable, reliable, parallel, distributed workflows
_pipeline = pipeline(
    do_something("One"),
    do_something("Two"),
    do_something("Three"),
    fork([
        do_something("Four"),
        do_something("Five"),
    ]))

_parallel = parallel([
    _pipeline,
    do_something("Two"),
    do_something("Three")])

_funnel = funnel([
    do_something("One"),
    _parallel,
    do_this("Three")])

print("FUNNEL: ", _funnel(do_this("Four")).get())
