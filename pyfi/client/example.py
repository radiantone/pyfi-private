from pyfi.client.api import Processor, Socket, Plug

# Create a processor
processor = Processor(name='proc1', module='pyfi.processors.sample', branch='main',
                      gitrepo='https://github.com/radiantone/pyfi-processors#egg=pyfi-processor')

processor2 = Processor(name='proc2', module='pyfi.processors.sample', hostname='radiant', branch='main',
                      gitrepo='https://github.com/radiantone/pyfi-processors#egg=pyfi-processor')


# Create a socket for that processor
do_something = Socket(name='proc1.socket1', processor=processor, queue={
                'name': 'pyfi.queue1'}, task='do_something')


do_this = Socket(name='proc1.socket2', processor=processor2, queue={
    'name': 'pyfi.queue2'}, task='do_this')
    
plug = Plug(name='plug1', queue={
    'name': 'pyfi.queue2'}, processor=processor, socket=do_this)

# Send a message to a socket
do_something("Hello World !")

#do_this("Do this!!")

'''
pyfi add plug -n plug1 -q pyfi.queue2 -pn proc1
pyfi add plug -n plug3 -q pyfi.queue3 -pn proc1
pyfi add processor -n proc2 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample  -h radiant
pyfi add socket -n proc2.socket1 -q pyfi.queue2 -pn proc2 -t do_this 
'''
