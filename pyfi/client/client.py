from pyfi.processor import Processor

processor = Processor(queue='pyfi.queue1.proc1', name='pyfi.processors.sample.do_something')

while True:
   processor("Hello World!")
   print("Hello World!")
   break
