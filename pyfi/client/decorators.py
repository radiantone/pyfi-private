from functools import wraps
from pyfi.client.api import Node, Agent, Worker, Processor, Socket, Plug, Task, Network

from pyfi.client.user import USER

class processor1(object):
    def __init__(self, arg):
        self._arg = arg

    def __call__(self, a, b):
        retval = self._arg(a, b)
        return retval ** 2

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


def processor(*args, **kwargs):
    print("processor called ", args, kwargs)

    model = stack.pop()

    if isinstance(model, Agent):
        kwargs['hostname'] = model.hostname
        
    kwargs['user'] = USER
    _proc = Processor(**kwargs)
    stack.append(_proc)

    processors[kwargs['name']] = _proc

    def decorator(klass, **dkwargs):

        pname = kwargs['module']+'.'+klass.__name__
        print("processor class", klass, pname)
        
        print("Created processor ",_proc)
        return _proc

    return decorator


def network(*args, **kwargs):
    print("network called ", kwargs)

    _network = Network(**kwargs)
    stack.append(_network)

    def decorator(node,*dargs,**dkwargs):
        _network.network.nodes += [node.node]

        return node

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
            worker = Worker(hostname=kwargs['hostname'], agent=_agent.agent, name=kwargs['name']+'.worker1', processor=processor.processor)
            _agent.agent.workers += [worker.worker]
        if isinstance(processor, Worker):
            _agent.agent.workers += [processor.worker]
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
