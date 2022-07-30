# do_something is my python function mounted onto a processor from my github repo
from pyfi.client.api import funnel, parallel, pipeline
from pyfi.client.example.api import do_something

# Send a message to the socket function
result = do_something("Inner " + str(do_something("Hello World XXX!")))

print("Result is: ", result)

_pipeline = pipeline(
    [
        do_something.p("One"),
        do_something.p("Two"),
        parallel(
            [
                do_something.p("Four"),
                do_something.p("Five"),
            ]
        ),
        do_something.p("Three"),
    ]
)

print("PIPELINE:", _pipeline().get())

_parallel = parallel([_pipeline, do_something.p("Two"), do_something.p("Three")])

_funnel = funnel([do_something.p("One"), _parallel, do_something.p("Three")])(
    do_something.p("Four")
)

print("FUNNEL: ", _funnel.get())
