""" Example"""
from pyfi.client.api import funnel, parallel, pipeline

# Function API over your processor models
# do_something is my python function mounted onto a processor from my github repo
from pyfi.client.example.api import do_something_p as do_something
from pyfi.client.example.api import do_this_p as do_this

# Durable, reliable, parallel, distributed workflows
_pipeline = pipeline(
    do_something("One"),
    do_something("Two"),
    parallel(
        [
            do_something("Four"),
            do_something("Five"),
        ]
    ),
    do_something("Three"),
)

_parallel = parallel([do_something("Six"), do_something("Seven"), _pipeline])

_funnel = funnel([_parallel, do_something("Eight"), do_this("Nine")])

print("FUNNEL: ", _funnel(do_this("Ten")).get())
# print("_pipeline: ", _parallel().get())
# print("_pipeline: ", _parallel().get())
