from pyfi.processor import Processor

processor = Processor(queue='pyfi.queue1.proc1',
                      name='pyfi.processors.sample.do_something')

while True:
    message = "Hello World !"
    processor(message)
    print(message)
    break
