from example12 import ProcessorA

from pyfi.client.api import parallel, pipeline, where

proca = ProcessorA()

print("Hi!", proca.do_something(proca.get_message()))

do_something = proca.do_something.p

# Asynchronous workflow
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
result = _pipeline()
print("Task Status", result.status)
print("Task ID", result.id)
print("Do other stuff")

print(result.get())

print("Using pipes")

_pipeline = parallel([do_something("One"), do_something("Two"), do_something("Three")])

workflow = _pipeline()

result = workflow.get()

r = list(result | where(lambda g: g["graph"]["value"] > 2))
print(r)
