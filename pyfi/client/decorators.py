from functools import wraps


class processor1(object):
    def __init__(self, arg):
        self._arg = arg

    def __call__(self, a, b):
        retval = self._arg(a, b)
        return retval ** 2


def task(name="", module="", processor=None, gitrepo=""):
    def wrapper_func(func):
        func()

    return wrapper_func


def processor2(*args, **kwargs):
    # decoration body - doing nothing really since we need to wait until the decorated object is instantiated
    print("processor called ", args, kwargs)

    class Processor:
        def __init__(self, *args, **kwargs):
            print(f"__init__() called with args: {args} and kwargs: {kwargs}")
            self.decorated_obj = Cls(*args, **kwargs)

        def __getattribute__(self, s):
            try:
                x = super().__getattribute__(s)
                return x
            except AttributeError:
                pass
            x = self.decorated_obj.__getattribute__(s)
            if type(x) == type(self.__init__):  # it is an instance method
                print(f"attribute belonging to decorated_obj: {s}")
                # this is equivalent of just decorating the method with time_this
                return task(x)
            else:
                return x

    return Processor  # decoration ends here


def processor(*args, **kwargs):
    print("processor called ", args, kwargs)

    def decorator(klass, **kwargs):
        print("processor class", klass, **kwargs)

        class Processor:
            """Populate methods of klass as tasks"""

            cls = None

            def __init__(self, *args, **kwargs):
                print(f"__init__() called with args: {args} and kwargs: {kwargs}")
                self.decorated_obj = klass(*args, **kwargs)

            def __getattribute__(self, s):
                try:
                    x = super().__getattribute__(s)
                    return x
                except AttributeError:
                    pass
                x = self.decorated_obj.__getattribute__(s)
                if type(x) == type(self.__init__):  # it is an instance method
                    print(f"attribute belonging to decorated_obj: {s}")
                    # this is equivalent of just decorating the method with time_this
                    return task(x)
                else:
                    return x

        Processor.cls = klass
        return Processor

    return decorator


class Agent:
    """Populate methods of klass as tasks"""

    cls = None

    def __init__(self, worker, *args, **kwargs):
        self.worker = worker
        print(f"   Agent instance with args: {args} and kwargs: {kwargs}")


def node(*args, **kwargs):
    print("node called ", kwargs)

    def decorator(processor):

        if isinstance(processor, Agent):
            print("node:agent", processor, processor.worker)
        else:
            print("node:processor", processor)

        """
        Either processor is of type Processor or Agent
        If it is an Agent class then it will have Agent.Worker.Processor
        """

        return processor

    return decorator


def agent(*args, **kwargs):
    print("agent called ", args, kwargs)
    _kwargs = kwargs

    def decorator(worker, **kwargs):
        print("agent:worker", worker, worker.processor.cls)

        return Agent(worker, **_kwargs)

    return decorator


def worker(*args, **kwargs):

    print("worker called ", args, kwargs)

    def decorator(processor):
        print("worker:processor", processor)

        class Worker:
            """Worker"""

            cls = None

            def __init__(self, processor, *args, **kwargs):
                print(f"   worker instance with args: {args} and kwargs: {kwargs}")
                self.processor = processor

        return Worker(processor)

    return decorator


def socket(*args, **kwargs):

    print("socket called ", args, kwargs)

    def decorator(task):
        print("socket:task", task)

        class Socket:
            """Worker"""

            cls = None

            def __init__(self, task, *args, **kwargs):
                print(f"   worker instance with args: {args} and kwargs: {kwargs}")
                self.task = task

        return Socket(task)

    return decorator


def plug(*args, **kwargs):

    print("plug called ", args, kwargs)

    def decorator(socket):
        print("plug:socket", socket)

        class Plug:
            """Worker"""

            cls = None

            def __init__(self, socket, *args, **kwargs):
                print(f"   worker instance with args: {args} and kwargs: {kwargs}")
                self.socket = socket

        return Plug(socket)

    return decorator
