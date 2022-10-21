'''
from celery.signals import (
    after_task_publish,
    setup_logging,
    task_failure,
    task_internal_error,
    task_postrun,
    task_prerun,
    task_received,
    task_success,
    worker_process_init,
)


class Script:
    def __init__(self, *args, **kwargs):

        # If processor is script
        self.func = self.celery.task(
            self.wrapped_function,
            name=self.processor.module + "." + socket.task.name,
            retries=self.processor.retries,
        )

    def execute(self):
        pass

    def wrapped_function(self, *args, **kwargs):
        """Main meta function that tracks arguments and dispatches to the user code"""
        import json

        redisclient = redis.Redis.from_url(self.backend)

        logging.info("WRAPPED FUNCTION INVOKE %s", socket.task)
        logging.info("ARGS: %s, KWARGS: %s", args, kwargs)

        taskid = kwargs["myid"]

        _kwargs = kwargs["kwargs"] if "kwargs" in kwargs else None

        if "argument" in kwargs:
            argument = kwargs["argument"]

            # Store argument in redis
            logging.info("ARGS %s %s %s", type(args), args, *args)

            # We are receiving an argument as a tuple, therefore only the first
            # element of the tuple is our data
            _argdata = args[0]
            _jsonargdata = json.dumps(_argdata)

            logging.info(
                "STORING ARGUMENT  %s %s",
                argument["key"]
                + "."
                + argument["name"]
                + "."
                + str(argument["position"]),
                _jsonargdata,
            )
            redisclient.set(
                argument["key"]
                + "."
                + argument["name"]
                + "."
                + str(argument["position"]),
                _jsonargdata,
            )

            # args = redisclient.get(argument['key']+'.*')
            # Compare args names to task arguments and if they are 1 to 1
            # then trigger the function
            logging.info("WRAPPED FUNCTION ARGUMENT %s ", argument)

            # If we received an argument and not all the arguments needed have been stored
            # then we simply return the argument, otherwise we execute the function
            _newargs = []
            for arg in socket.task.arguments:
                if (
                    arg.kind != Parameter.POSITIONAL_ONLY
                    and arg.kind != Parameter.POSITIONAL_OR_KEYWORD
                ):
                    continue

                _argdata = redisclient.get(
                    argument["key"] + "." + arg.name + "." + str(arg.position)
                )

                if _argdata is None:
                    logging.info(
                        "ARGUMENT NOT SATISIFIED %s",
                        argument["key"] + "." + arg.name + "." + str(arg.position),
                    )
                    return argument
                else:
                    _arg = json.loads(_argdata)
                    logging.info(
                        "FOUND STORED ARGUMENT %s %s",
                        _arg,
                        argument["key"] + "." + arg.name + "." + str(arg.position),
                    )
                    _newargs.append(_arg)
                logging.info("WRAPPED_FUNCTION ARG: %s", arg)

            args = _newargs

        source = inspect.getsource(execute_function)
        _call = 'execute_function("{}", "{}", "{}")'.format(
            taskid, socket.task.module, socket.task.name
        )

        import pickle

        if _kwargs:
            """If we have kwargs to pass in"""
            logging.info("Invoking function %s %s", args, _kwargs)

            if self.container and self.processor.use_container:
                # Run function in container and get result
                with open("out/" + taskid + ".py", "w") as pfile:
                    pfile.write(source + "\n")
                    pfile.write(_call + "\n")

                if self.processor.detached:
                    # Run command inside self.container passing in task id, module and function
                    pythoncmd = "python /tmp/" + taskid + ".py"
                    logging.info("Invoking %s", pythoncmd)

                    self.container.exec_run(pythoncmd)

                    # Unpickle output and return it
                else:
                    # Run new non-detached container for task
                    raise NotImplementedError
            else:
                return _func(*args, **_kwargs)
        else:
            """If we only have args to pass in"""
            logging.info("Invoking function %s", args)

            if self.container and self.processor.use_container:
                # Run function in container and get result
                with open("out/" + taskid + ".py", "w") as pfile:
                    pfile.write(source + "\n")
                    pfile.write(_call + "\n")

                if self.processor.detached:
                    # Run command inside self.container
                    with open("out/" + taskid + ".kwargs", "wb") as kwargsfile:
                        pickle.dump(kwargs, kwargsfile)
                    with open("out/" + taskid + ".args", "wb") as argsfile:
                        pickle.dump(args, argsfile)

                    pythoncmd = "python /tmp/" + taskid + ".py"
                    logging.info("Invoking %s", pythoncmd)

                    res = self.container.exec_run(pythoncmd)

                    logging.info("OUTPUT: %s", res.output)

                    result = None
                    with open("out/" + taskid + ".out", "rb") as outfile:
                        result = pickle.load(outfile)

                    try:
                        """Remove state files"""
                        os.remove("out/" + taskid + ".kwargs")
                        os.remove("out/" + taskid + ".args")
                        os.remove("out/" + taskid + ".out")
                    except Exception as ex:
                        logging.warning(ex)
                    finally:
                        return result

                else:
                    raise NotImplementedError
            else:
                return _func(*args)

    @task_prerun.connect()
    def pyfi_task_prerun(self, sender=None, task=None, task_id=None, *args, **kwargs):
        """Update args and kwargs before sending to task. Other bookeeping"""
        from datetime import datetime
        from uuid import uuid4

        # PRERUN_CONDITION.acquire()
        try:
            print("prerun TASK: ", type(task), task, kwargs)

            if sender.__name__ == "enqueue":
                return

            _function_name = task.name.rsplit(".")[-1:]
            print(
                "KWARGS:",
                {
                    "signal": "prerun",
                    "sender": _function_name[0],
                    "kwargs": kwargs["kwargs"],
                    "taskid": task_id,
                    "args": args,
                },
            )
            self.main_queue.put(
                {
                    "signal": "prerun",
                    "sender": _function_name[0],
                    "kwargs": kwargs["kwargs"],
                    "taskid": task_id,
                    "args": args,
                }
            )

            if "tracking" not in kwargs.get("kwargs"):
                kwargs["kwargs"]["tracking"] = str(uuid4())

            logging.info("Waiting on PRERUN REPLY")
            response = self.prerun_queue.get()
            logging.info("GOT PRERUN QUEUE MESSAGE %s", response)
            if "error" in response:
                logging.error(response["error"])
            else:
                kwargs["kwargs"].update(response)
            kwargs["kwargs"]["output"] = {}

            logging.info("PRERUN QUEUE: %s", response)
            logging.info("PRERUN KWARGS IS NOW: %s", kwargs)

            if "argument" in kwargs["kwargs"]:
                _argument = kwargs["kwargs"]["argument"]
                key = _argument["key"]
            # If this is an argument call, then check redis for all current arguments
            # Including the one here, pull in all the arguments and put them in the kwargs
            # The wrapped_function will receive them and based on the function arguments
            # decide if it can invoke the function or not

        finally:
            # PRERUN_CONDITION.release()
            pass

    @task_success.connect()
    def pyfi_task_success(sender=None, **kwargs):
        logging.info("Task SUCCESS: %s", sender)
        # Store task run data
        pass

    @task_failure.connect()
    def pyfi_task_failure(sender=None, **kwargs):
        # Store task run data
        pass

    @task_internal_error.connect()
    def pyfi_task_internal_error(sender=None, **kwargs):
        # Store task run data
        pass

    @task_received.connect()
    def pyfi_task_received(sender=None, request=None, **kwargs):
        logging.info("Task RECEIVED REQUEST %s %s %s", request.id, sender, request.name)

        _function_name = request.name.rsplit(".")[-1:]
        logging.info("Task Request Parent %s", request.parent_id)
        from datetime import datetime
        from uuid import uuid4

        sender = request.task_name.rsplit(".")[-1]
        print("RECEIVED SENDER:", sender)

        if sender == "enqueue":
            return

        print("KWARGS", kwargs)
        print(
            "RECEIVED KWARGS:",
            {
                "signal": "received",
                "sender": _function_name[0],
                "kwargs": {},
                "request": request.id,
                "taskparent": request.parent_id,
                "taskid": request.id,
            },
        )
        self.main_queue.put(
            {
                "signal": "received",
                "sender": _function_name[0],
                "kwargs": {},
                "request": request.id,
                "taskparent": request.parent_id,
                "taskid": request.id,
            }
        )
        print("PUT RECEIVED KWARGS on queue")

        # Wait for reply
        print("WAITING ON received_queue")
        _kwargs = self.received_queue.get()
        kwargs.update(_kwargs)
        print("GOT RECEIVED REPLY ", _kwargs)
        print("New KWARGS ARE:", kwargs)

    @task_postrun.connect()
    def pyfi_task_postrun(
        sender=None, task_id=None, task=None, retval=None, *args, **kwargs
    ):
        from datetime import datetime
        from uuid import uuid4

        if sender.__name__ == "enqueue":
            return

        _function_name = task.name.rsplit(".")[-1:][0]
        logging.info("TASK POSTRUN ARGS: %s", args)
        logging.info("TASK POSTRUN RETVAL: %s", retval)
        logging.info(
            "TASK_POSTRUN KWARGS: %s",
            {
                "signal": "postrun",
                "result": retval,
                "sender": _function_name,
                "kwargs": kwargs["kwargs"],
                "taskid": task_id,
                "args": args,
            },
        )

        logging.info("POSTRUN PUTTING ON main_queue")
        self.main_queue.put(
            {
                "signal": "postrun",
                "result": retval,
                "sender": _function_name,
                "kwargs": kwargs["kwargs"],
                "taskid": task_id,
                "args": args,
            }
        )
        logging.info("POSTRUN DONE PUTTING ON main_queue")

'''
