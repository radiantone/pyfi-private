""" Example workflow primitives """

# Import workflow primitives
from pyfi.client.api import parallel, select, where

# Import socket functions
from pyfi.client.example.api import do_something_p as do_something

# Define a parallel workflow
_pipeline = parallel([do_something("One"), do_something("Two"), do_something("Three")])

# Execute the workflow, which invokes the functions wherever they may be located
# Return a delayed/promise
workflow = _pipeline()

# Wait for the result synchronously
result = workflow.get()

import json

print(json.dumps(result, indent=4))

# Filter the results where value > 5
r = list(result | where(lambda g: g["graph"]["value"] > 5))
print(r)

# Create a list of do_something functions after filtering the results
r = list(
    result
    | where(lambda g: g["graph"]["value"] > 2)
    | select(lambda g: do_something(g["message"]))
)
print(r)

# Execute the parallel list of do_something calls
_par2 = parallel(r)

# Wait for the result
result = _par2().get()

# Print result
print(json.dumps(result, indent=4))
