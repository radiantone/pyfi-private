""" Example"""
from pyfi.client.api import funnel, parallel, pipeline
from pyfi.client.example.api import do_something_p as do_something

_pipeline = pipeline(
    [
        do_something("One"),
        do_something("Two"),
        parallel(
            [
                do_something("Four"),
                do_something("Five"),
            ]
        ),
        do_something("Three"),
    ]
)

_funnel = funnel(do_something("A"))

pip = _pipeline()
pip.get()
# fr = _funnel(_pipeline)
# print("FUNNEL: ", fr.get())
for result, value in pip.collect(intermediate=True):
    print(result, value)
print("GRAPH:", pip.parent.parent.graph)
