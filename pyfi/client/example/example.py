from pyfi.client.api import Processor, Socket, Plug

# Create a processor
processor = Processor(name='proc1', beat=True, module='pyfi.processors.sample', branch='main',
                      gitrepo='https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor')

processor2 = Processor(name='proc2', module='pyfi.processors.sample', hostname='agent1', branch='main',
                       gitrepo='https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor')


# Create a socket for that processor
do_something = Socket(name='pyfi.processors.sample.do_something', interval=10, processor=processor, queue={
                'name': 'pyfi.queue1'}, task='do_something')

do_this = Socket(name='pyfi.processors.sample.do_this', processor=processor2, queue={
    'name': 'pyfi.queue2'}, task='do_this')
    
plug = Plug(name='plug1', queue={
    'name': 'pyfi.queue2'}, processor=processor, socket=do_this)

# Send a message to a socket(function)
result = do_something("Hello World !")
print("RESULT",result)
