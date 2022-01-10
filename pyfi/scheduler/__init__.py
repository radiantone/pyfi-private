import logging
import os
import platform
import time
import sched
import signal
import sys

from multiprocessing import Process

from pyfi.db.model import SchedulerModel, WorkModel, ProcessorModel

HOSTNAME = platform.node()

if "PYFI_HOSTNAME" in os.environ:
    HOSTNAME = os.environ["PYFI_HOSTNAME"]

class SchedulerPlugin:
    """ Base scheduler plugin class """
    context = None
    interval = None
    name = None
    _stop = False

    def run(self, *args, **kwargs):
        logging.info("Schedule run %s %s",args,kwargs)

    def stop(self):
        logging.info("Stopping {}".format(self.name))
        self._stop = True
        self.s.cancel(self.event)

    def start(self, name, context, interval, *args, **kwargs):
        import threading
        
        self.context = context
        self.interval = interval
        self.name = name

        logging.info("Plugin starting...")
        self.thread = thread = threading.Thread(target=self.schedule, args=(self.interval,self.run,args))
        thread.start()

    def schedule(self, interval,func,args=(),priority=1):
        self.s = s = sched.scheduler(time.time, time.sleep)
        self.periodic_task(s,interval,func,args,priority)
        s.run()

    def periodic_task(self, scheduler,interval,func,args,priority):
        func(*args)
        if self._stop:
            return

        self.event = scheduler.enter(interval,priority,self.periodic_task,
                        (scheduler,interval,func,args,priority))

class NodePlugin(SchedulerPlugin):
    """ Enforce agent status on nodes """
    def run(self, *args, **kwargs):
        import requests

        logging.info("NodePlugin: Schedule run %s %s",args,kwargs)

        scheduler = (
            self.context.obj["database"]
            .session.query(SchedulerModel)
            .filter_by(name=self.name)
            .first()
        )

        # These are my nodes to manage
        if scheduler.nodes:
            for node in scheduler.nodes:

                # For each node->agent determine if it is running and if not ssh into host and
                # run the agent. The agent worker will then notice any processors assigned to it
                # and launch those processors on its own

                """Calculate any changes needed by inspecting the nodes, agents, workers, etc"""
                """ If changes are needed, put read lock on table and make change """
                logging.info("Node %s", node)
                agent = node.agent

                logging.info("Agent %s CPUs", agent.cpus)
                try:
                    result = requests.get("http://" + agent.hostname + ":8002")
                    if result.status_code == 200:
                        logging.info("Agent is alive.")
                    else:
                        raise
                except:
                    logging.info("Agent is down.")
                # If there are processors pending relocation, calculate if there
                # are free CPUs under this agent byt adding all the active processors
                # If there are, then move the processor to this agent and node.h

                processor = agent.worker.processor
                logging.info(
                    "Processor %s %s CPU workers", processor.name, processor.concurrency
                )

                # Look at all the processors for this node, if the total CPUs exceeds the nodes CPUs
                # Then determine which processor to find a better home

                # Or, for example, if you have two nodes A and B and B has 2 processors but A has none,
                # The scheduler will move one of the processors to A if A node has enough CPUs

                # Processors with 6 sockets would optimally want a node with 6 CPUs so each socket task
                # can run on its own core. This allows the scheduler to determine the compute needs for
                # each processor and locate it accordingly.

            # Perform read lock of processors without hostnames
            # Put processors in pending list to be assigned below
            # if there are available nodes, otherwise release the read lock
            try:
                # These are processors without an node to run on currently
                orphaned_processors = (
                    self.context.obj["database"]
                    .session.query(ProcessorModel)
                    .filter_by(hostname=None)
                    .with_for_update()
                    .all()
                )

                for processor in orphaned_processors:
                    logging.info("Finding home for orphaned processor %s", processor)

                    # Scan my nodes and agents looking for space or rearranging for space

            finally:
                self.context.obj["database"].session.commit()

class DeployProcessorPlugin(SchedulerPlugin):
    """ Enforce, create, move, delete deployments """
    def run(self, *args, **kwargs):
        logging.info("DeployProcessorPlugin: Schedule run %s, %s",args,kwargs)
        logging.info("Fetching processors to be deployed")
        processor = (
            self.context.obj["database"]
            .session.query(ProcessorModel)
            .filter_by(requested_status="deploy")
            .with_for_update()
            .first()
        )

        if processor:
            logging.info("Deploying processor %s", processor)
            if len(processor.deployments) == 0:
                # I need to add deployments for this processor

                # Look across my nodes and agents for cpus
                # subtract running workers with concurrency to get free cpus for that node
                # If no node can host all the cpus for the deployment, then create
                # separate deployments with smaller cpus spread across nodes
                pass

class WorkPlugin(SchedulerPlugin):
    """ Process work records, which are queued or scheduled tasks """
    def run(self, *args, **kwargs):
        logging.info("WorkPlugin: Schedule run %s %s",args,kwargs)
        logging.info("WorkPlugin: Fetching work")
        all_work = self.context.obj["database"].session.query(WorkModel).all()

        for work in all_work:
            # Determine the work request and schedule or run it
            # Assign the workmodel to a worker
            logging.info("WorkPlugin: Found work %s", work)

_plugins = [NodePlugin,DeployProcessorPlugin,WorkPlugin]

class BasicScheduler:
    """ Basic Scheduler """

    process = None
    nodes = []

    def __init__(self, context, name, interval):

        self.context = context
        self.name = name
        self.interval = interval

        self.plugins = [cls() for cls in _plugins]

        signal.signal(signal.SIGINT, self.stop)

    def stop(self, *args, **kwargs):
        [plugin.stop() for plugin in self.plugins]
        logging.info("Stopped")

    def run(self):
        [plugin.start(self.name, self.context, self.interval) for plugin in self.plugins]
        logging.info("Started")


    def start(self):
        self.process = Process(target=self.run)
        self.process.daemon = True

        return self.process
