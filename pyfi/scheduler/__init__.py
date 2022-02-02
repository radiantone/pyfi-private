import logging
import os
import platform
import time
import sched
import signal
import sys

from multiprocessing import Process

from pyfi.db.model import SchedulerModel, WorkModel, ProcessorModel, DeploymentModel
from pyfi.db import get_session

HOSTNAME = platform.node()

if "PYFI_HOSTNAME" in os.environ:
    HOSTNAME = os.environ["PYFI_HOSTNAME"]


class SchedulerPlugin:
    """Base scheduler plugin class"""

    context = None
    interval = None
    name = None
    _stop = False
    event = None

    def run(self, *args, **kwargs):
        logging.info("Schedule run %s %s", args, kwargs)

    def stop(self):
        logging.info("Stopping {}".format(self.name))
        self._stop = True

        if self.event:
            try:
                self.s.cancel(self.event)
            except:
                pass

    def start(self, name, interval, *args, **kwargs):
        import threading

        self.interval = interval
        self.name = name

        logging.info("Plugin starting...")
        self.thread = thread = threading.Thread(
            target=self.schedule, args=(self.interval, self.run, args)
        )
        thread.start()

    def schedule(self, interval, func, args=(), priority=1):
        self.s = s = sched.scheduler(time.time, time.sleep)
        self.periodic_task(s, interval, func, args, priority)
        s.run()

    def periodic_task(self, scheduler, interval, func, args, priority):
        func(*args)
        if self._stop:
            return

        self.event = scheduler.enter(
            interval,
            priority,
            self.periodic_task,
            (scheduler, interval, func, args, priority),
        )


class NodePlugin(SchedulerPlugin):
    """Enforce agent status on nodes"""

    def run(self, *args, **kwargs):
        import requests
        session = get_session()
        try:
            logging.info("NodePlugin: Schedule run %s %s", args, kwargs)

            scheduler = (
                session.query(SchedulerModel)
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
                        logging.debug("Agent is down.")
                    # If there are processors pending relocation, calculate if there
                    # are free CPUs under this agent byt adding all the active processors
                    # If there are, then move the processor to this agent and node.h

                    for worker in agent.workers:
                        processor = worker.processor
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
        finally:
            session.close()


class DeployProcessorPlugin(SchedulerPlugin):
    """Enforce, create, move, delete deployments"""

    def run(self, *args, **kwargs):

        session = get_session()
        try:

            logging.info("DeployProcessorPlugin: Schedule run %s, %s", args, kwargs)
            logging.info("Fetching processors to be deployed")
            processor = (
                session.query(ProcessorModel)
                #.filter_by(requested_status="deploy")
                .with_for_update()
                .first()
            )
            logging.info("Processor is %s", processor)
            if processor:
                logging.info("Deploying processor %s", processor)
                if len(processor.deployments) == 0:
                    # I need to add deployments for this processor

                    # Look across my nodes and agents for cpus
                    # subtract running workers with concurrency to get free cpus for that node
                    # If no node can host all the cpus for the deployment, then create
                    # separate deployments with smaller cpus spread across nodes
                    pass

                scheduler = (
                    session.query(SchedulerModel)
                    .filter_by(name=self.name)
                    .first()
                )

                # For this processor, determine how many deployments are needed to satisfy the concurrency parameter
                # Each node will have n free CPUs. A set of deployments are needed that map the processor concurrency needs
                # to all available CPUs across nodes.
                logging.info("Processor concurrency is %s", processor.concurrency)

                deployed_cpus = 0
                for deployment in processor.deployments:
                    logging.info("   Deployment: CPU %s", deployment.cpus)
                    deployed_cpus += deployment.cpus            

                if deployed_cpus < processor.concurrency:
                    needed_cpus = processor.concurrency - deployed_cpus
                    logging.info("Concurrency shortfall, finding %s CPUs", needed_cpus)

                    if scheduler.nodes:
                        for node in scheduler.nodes:
                            agent = node.agent
                            logging.info("Agent for node %s has %s cpus", node.hostname, agent.cpus)

                            worker_cpus = 0
                            for worker in agent.workers:
                                logging.info("Agent worker with %s cpus", worker.concurrency)
                                if worker.deployment:
                                    worker_cpus += worker.deployment.cpus

                            logging.info("Agent %s is using %s of its %s cpus", agent.name, worker_cpus, agent.cpus)

                            if agent.cpus - worker_cpus >= 1:
                                _cpus = agent.cpus - worker_cpus
                                if _cpus > needed_cpus:
                                    _cpus = needed_cpus
                                if _cpus > 0:
                                    logging.info("Creating new deployment for %s CPUS", _cpus)
                                    _deployment = DeploymentModel(cpus=_cpus, processor=processor, name=processor.name+".deploy"+str(len(processor.deployments)), hostname=node.hostname)
                                    session.add(_deployment)
                                    logging.info("Deploying processor to node %s with %s cpus", node, _cpus)
                                    session.commit()
                                    needed_cpus -= _cpus
                                else:
                                    logging.warning("_cpus is zero")

                else:
                    logging.info("Processor concurrency needs are met.")
        finally:
            session.close()

class WorkPlugin(SchedulerPlugin):
    """Process work records, which are queued or scheduled tasks"""

    def run(self, *args, **kwargs):
        session = get_session()
        try:

            logging.info("WorkPlugin: Schedule run %s %s", args, kwargs)
            logging.info("WorkPlugin: Fetching work")
            all_work = session.query(WorkModel).all()

            for work in all_work:
                # Determine the work request and schedule or run it
                # Assign the workmodel to a worker
                logging.info("WorkPlugin: Found work %s", work)
        finally:
            session.close()


_plugins = [NodePlugin, DeployProcessorPlugin, WorkPlugin]


class BasicScheduler:
    """Basic Scheduler"""

    process = None
    nodes = []

    def __init__(self, name, interval):

        self.name = name
        self.interval = interval

        self.plugins = [cls() for cls in _plugins]

        signal.signal(signal.SIGINT, self.stop)

    def stop(self, *args, **kwargs):
        [plugin.stop() for plugin in self.plugins]
        logging.info("Stopped")

    def run(self):
        [
            plugin.start(self.name, self.interval)
            for plugin in self.plugins
        ]
        logging.info("Started")

    def start(self):
        self.process = Process(target=self.run)
        self.process.daemon = True

        return self.process
