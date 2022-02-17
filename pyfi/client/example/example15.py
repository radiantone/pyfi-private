from example12 import ProcessorA

proca = ProcessorA()

res = proca.do_something.get(taskid="10d7bfcf-680d-4061-817c-787f12092d67")
print("Task ID", res.id)
print("Status", res.status)
print("Result", res.get())
