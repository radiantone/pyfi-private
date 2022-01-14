import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
from functools import wraps
from pyfi.client.api import Node, Agent, Worker, Processor, Socket, Plug, Task, Network, Deployment

from pyfi.client.user import USER

stack = []
processors = {}
nodes = {}
agents = {}
workers = {}
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
            
        logging.debug("TheMeta init")
        super(TheMeta, cls).__init__(name, bases, dct)

class ProcessorBase:
    __metaclass__ = TheMeta

    def __init__(self):
        import types


        logging.debug("ProcessorBase init")
        logging.debug("ProcessorBase: sockets: %s",self.__sockets__)
        # TODO: Patch instance methods with Socket calls
        for socket in self.__sockets__:
            def wait(self, *args, taskid=None):
                """ Given the taskid, return an asynchronous result """
                print("Waiting on",taskid)
                return "Waited result"

            def socket_dispatch(*args, **kwargs):
                """ In place of the original class method, dispatch to the socket """
                logging.debug("socket_dispatch")
                _sock = Socket(name=socket.name, user=USER).p
                return _sock

            _function = types.MethodType(socket_dispatch, self)
            _sock = Socket(name=socket.name, user=USER)
            _wait = types.MethodType(wait, _sock)
            setattr(_sock,'wait',_wait)
            setattr(self,socket.task.name,_sock )
        

def processor(*args, **kwargs):
    logging.debug("processor called %s %s", args, kwargs)

    model = stack.pop()
    logging.debug("processor:agent %s",model)
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
        logging.debug("Deploment added %s",_deployment.deployment.name)

    def decorator(klass, **dkwargs):

        pname = kwargs['module']+'.'+klass.__name__
        logging.debug("processor class %s %s", klass, pname)
        _proc.cls = klass
        logging.debug("Created processor %s ",_proc)
        # TODO: Instrument _proc.cls and monkey patch new
        # method 'task' that creates and returns the associated socket
        setattr(klass,'__metaclass__',TheMeta)
        logging.debug("Instrumenting class {}:{} from {}".format(_proc, klass.__metaclass__, klass))
        for socket in _proc.processor.sockets:
            logging.debug("processor:socket %s ",socket)
        
        setattr(klass,'__sockets__',_proc.processor.sockets)
        setattr(klass,'__processor__',_proc)
        logging.debug("processor:returning: %s ",klass)
        return klass

    return decorator


def network(*args, **kwargs):
    logging.debug("network called  %s ", kwargs)

    _network = Network(**kwargs)
    stack.append(_network)

    def decorator(node,*dargs,**dkwargs):
        logging.debug("network:%s adding node %s",_network.network.name,node.node.name)
        _network.network.nodes += [node.node]
        _network.session.commit()
        return node.agent._processor

    return decorator

def node(*args, **kwargs):
    logging.debug("node called  %s ", kwargs)

    _node = Node(**kwargs)
    stack.append(_node)

    def decorator(model,*dargs,**dkwargs):
        logging.debug("node:agent %s ", model)

        logging.debug("---->Agent workers %s  %s ",model.agent.name, model.agent.workers)
        for worker in model.agent.workers:
            if worker.name.rsplit('.')[-1] == worker.processor.name:
                continue
            logging.debug("---->Worker processor %s ",worker.processor)
            logging.debug("====>Updating WORKER NAME %s ",worker.name)
            worker.name = worker.name+"."+worker.processor.name
            
        return _node

    return decorator


def agent(*args, **kwargs):
    logging.debug("agent called  %s  %s ", args, kwargs)

    node = stack.pop()
    kwargs['hostname'] = node.node.hostname
    kwargs['user'] = USER
    kwargs['node'] = node
    _agent = Agent(**kwargs)
    stack.append(_agent)
    node.agent = _agent

    def decorator(processor):
        logging.debug("agent:model %s ",processor)
        if getattr(processor,'__processor__'):
            _processor = processor.__processor__
            logging.debug("Creating worker: %s ",kwargs['name']+'.worker')
            worker = Worker(hostname=kwargs['hostname'], agent=_agent.agent, name=kwargs['name']+'.worker.'+_processor.name, processor=_processor.processor)
            workers[_processor.name] = worker
        elif isinstance(processor, Worker):
            _agent.agent.workers += [processor.worker]
        
        _agent._processor = processor
        return _agent

    return decorator


def worker(*args, **kwargs):

    logging.debug("worker called  %s  %s ", args, kwargs)

    kwargs['user'] = USER
    agent = stack.pop()
    _worker = Worker(hostname=agent.hostname, user=USER)
    agent.worker = _worker
    stack.append(_worker)

    def decorator(processor):
        logging.debug("worker:processor %s ", processor)

        return processor

    return decorator


def socket(*args, **kwargs):

    logging.debug("socket called  %s  %s ", args, kwargs)

    model = stack.pop()
    logging.debug("MODEL:  %s ",model)

    kwargs['user'] = USER
    def decorator(task):
        logging.debug("socket:task %s ", task)
        logging.debug("task:name %s ",task.__name__)
        #procname = task.__qualname__.rsplit('.')[0]
        _proc = processors[kwargs['processor']]
        logging.debug("socket:worker %s ",worker)
        logging.debug("socket:processor %s ",_proc)
        kwargs['processor'] = _proc
        kwargs['task'] = task.__name__
        _socket = Socket(**kwargs)
        sockets[_socket.name] = _socket

        return _socket

    return decorator


def plug(*args, **kwargs):

    logging.debug("plug called  %s %s", args, kwargs)

    model = stack.pop()
    logging.debug("PLUG POP:  %s ",model)

    stack.append(kwargs)

    def decorator(socket):
        logging.debug("plug:socket %s  %s ", socket, socket.task)
        target = Socket(name=kwargs['target'], processor=model, user=USER)

        _plug = Plug(name=kwargs['name'], queue=kwargs['queue'], source=socket, target=target, processor=socket.processor, user=USER)
        plugs[_plug.name] = _plug
        return _plug

    return decorator
