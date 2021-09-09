from pyfi.client.api import Processor, Socket, Plug

# Create a processor
processor = Processor(name='proc1', beat=True, module='pyfi.processors.sample', branch='main',
                      gitrepo='https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor')

processor2 = Processor(name='proc2', module='pyfi.processors.sample', hostname='agent1', branch='main',
                       gitrepo='https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor')


# Create a socket on the processor to receive requests for the do_something python function(task)
do_something = Socket(name='pyfi.processors.sample.do_something', interval=10, processor=processor, queue={'name': 'pyfi.queue1'}, task='do_something')

# Create a socket on the processor to receive requests for the do_this python function(task)
do_this = Socket(name='pyfi.processors.sample.do_this', processor=processor2, queue={'name': 'pyfi.queue2'}, task='do_this')
 
# Create a plug that connects one processor to a socket of another
plug = Plug(name='plug1', queue={'name': 'pyfi.queue2'}, processor=processor, source=do_something, target=do_this)

# Send a message to a socket(function). 
result = do_something("Hello World !")

print("RESULT",result)
