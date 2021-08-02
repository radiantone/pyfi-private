from pyfi.processor import Processor

processor = Processor(queue='pyfi.queue1', name='pyfi.processors.sample.do_something')

while True:
    #app.signature('pyfi.processors.sample.do_something', args=('Hello World!',),
    #              queue='pyfi.queue1', kwargs={}).delay()
    processor("Hello World!")
    print("Hello World!")
