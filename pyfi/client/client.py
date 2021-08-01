from pyfi.processor import Processor

processor = Processor('pyfi.queue1', 'pyfi.processors.sample.do_something')

result1 = processor('Hello World!')
#print("Calling processor 2")
#result2 = processor('It\'s me!')

print(result1.get())

#print(result2.get())
