from functools import wraps
from pyfi.client.api import Node, Agent, Worker, Processor, Socket, Plug, Task, Network, Deployment

from pyfi.client.user import USER

stack = []
processors = {}
nodes = {}
agents = {}
sockets = {}
plugs = {}
tasks = {}

def task(name="", module="", processor=None, gitrepo=""):
    def wrapper_func(func):
        func()

    return wrapper_func

class TheMeta(type):
    def __new__(meta, name, bases, attributes):
        # Check if args contains the number "42" 
        # or has the string "The answer to life, the universe, and everything"
        # If so, just return a pointer to an existing object:
        # Else, just create the object as it is:
        return super(TheMeta, meta).__new__(meta, name, bases, attributes)

    def __init__(cls, name, bases, dct):
            
        print("TheMeta init")
        super(TheMeta, cls).__init__(name, bases, dct)

class ProcessorBase:
    __metaclass__ = TheMeta

    def __init__(self):
        import types


        print("ProcessorBase init")
        print("ProcessorBase: sockets: ",self.__sockets__)
        # TODO: Patch instance methods with Socket calls
        for socket in self.__sockets__:

            def socket_dispatch(*args, **kwargs):
                print("socket_dispatch")
                _sock = Socket(name=socket.name, user=USER).p
                return _sock

            _function = types.MethodType(socket_dispatch, self)
            _sock = Socket(name=socket.name, user=USER)
            setattr(self,socket.task.name,_sock )
        

def processor(*args, **kwargs):
    print("processor called ", args, kwargs)

    model = stack.pop()

    if isinstance(model, Agent):
        kwargs['hostname'] = model.hostname
        
    kwargs['user'] = USER
    deploy = False
    if 'deploy' in kwargs and kwargs['deploy']:
        deploy = kwargs['deploy']
        del kwargs['deploy']

    _proc = Processor(**kwargs)
    stack.append(_proc)

    processors[kwargs['name']] = _proc
    if deploy:
        _deployment = Deployment(processor=_proc.processor, name=_proc.name+".d"+str(len(_proc.processor.deployments)), hostname=model.hostname)
        print("Deploment added",_deployment.deployment.name)

    def decorator(klass, **dkwargs):

        pname = kwargs['module']+'.'+klass.__name__
        print("processor class", klass, pname)
        _proc.cls = klass
        print("Created processor ",_proc)
        # TODO: Instrument _proc.cls and monkey patch new
        # method 'task' that creates and returns the associated socket
        setattr(klass,'__metaclass__',TheMeta)
        print("Instrumenting class {}:{} from {}".format(_proc, klass.__metaclass__, klass))
        for socket in _proc.processor.sockets:
            print("processor:socket",socket)
        
        setattr(klass,'__sockets__',_proc.processor.sockets)
        return klass

    return decorator


def network(*args, **kwargs):
    print("network called ", kwargs)

    _network = Network(**kwargs)
    stack.append(_network)

    def decorator(node,*dargs,**dkwargs):
        _network.network.nodes += [node.node]

        return node.agent._processor

    return decorator

def node(*args, **kwargs):
    print("node called ", kwargs)

    _node = Node(**kwargs)
    stack.append(_node)

    def decorator(model,*dargs,**dkwargs):
        print("node:agent", model)

        return _node

    return decorator


def agent(*args, **kwargs):
    print("agent called ", args, kwargs)

    node = stack.pop()
    kwargs['hostname'] = node.node.hostname
    kwargs['user'] = USER
    kwargs['node'] = node
    _agent = Agent(**kwargs)
    stack.append(_agent)
    node.agent = _agent

    def decorator(processor):
        print("agent:model",processor)
        if isinstance(processor, Processor):
            print("Creating worker:",kwargs['name']+'.worker'+str(len(_agent.agent.workers)))
            worker = Worker(hostname=kwargs['hostname'], agent=_agent.agent, name=kwargs['name']+'.worker'+str(len(_agent.agent.workers)), processor=processor.processor)
            _agent.agent.workers += [worker.worker]
        if isinstance(processor, Worker):
            _agent.agent.workers += [processor.worker]
        
        _agent._processor = processor
        return _agent

    return decorator


def worker(*args, **kwargs):

    print("worker called ", args, kwargs)

    kwargs['user'] = USER
    agent = stack.pop()
    _worker = Worker(hostname=agent.hostname, user=USER)
    agent.worker = _worker
    stack.append(_worker)

    def decorator(processor):
        print("worker:processor", processor)

        return processor

    return decorator


def socket(*args, **kwargs):

    print("socket called ", args, kwargs)

    model = stack.pop()
    print("MODEL: ",model)

    kwargs['user'] = USER
    def decorator(task):
        print("socket:task", task)
        print("task:name",task.__name__)
        #procname = task.__qualname__.rsplit('.')[0]
        _proc = processors[kwargs['processor']]
        print("socket:processor",_proc)
        kwargs['processor'] = _proc
        kwargs['task'] = task.__name__
        _socket = Socket(**kwargs)
        sockets[_socket.name] = _socket

        return _socket

    return decorator


def plug(*args, **kwargs):

    print("plug called ", args, kwargs)

    model = stack.pop()
    print("PLUG POP: ",model)

    stack.append(kwargs)

    def decorator(socket):
        print("plug:socket", socket, socket.task)
        target = Socket(name=kwargs['target'], processor=model, user=USER)

        _plug = Plug(name=kwargs['name'], queue=kwargs['queue'], source=socket, target=target, processor=socket.processor, user=USER)
        plugs[_plug.name] = _plug
        return _plug

    return decorator
