import configparser
import json
import logging
import os
import platform
import sched
import signal
import time
from multiprocessing import Process
from pathlib import Path

from celery import Celery
from pyfi.db import get_session
from pyfi.db.model import (
    AgentModel,
    DeploymentModel,
    NodeModel,
    ProcessorModel,
    QueueModel,
    SchedulerModel,
    TaskModel,
    WorkModel,
)

HOSTNAME = platform.node()

if "PYFI_HOSTNAME" in os.environ:
    HOSTNAME = os.environ["PYFI_HOSTNAME"]


HOME = str(Path.home())
CONFIG = configparser.ConfigParser()

# Load the config
if os.path.exists(HOME + "/pyfi.ini"):
    CONFIG.read(HOME + "/pyfi.ini")

backend = CONFIG.get("backend", "uri")
broker = CONFIG.get("broker", "uri")

celery = Celery(backend=backend, broker=broker)


class SchedulerPlugin:
    """Base scheduler plugin class"""

    context = None
    interval = None
    name = None
    _stop = False
    event = None

    def __init__(self,args):
        self.args = args

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

        logging.debug("Plugin %s starting...", name)
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
            logging.debug("NodePlugin: Schedule run %s %s", args, kwargs)

            scheduler = session.query(SchedulerModel).filter_by(name=self.name).first()

            # These are my nodes to manage
            if scheduler.nodes:
                for node in scheduler.nodes:

                    # For each node->agent determine if it is running and if not ssh into host and
                    # run the agent. The agent worker will then notice any processors assigned to it
                    # and launch those processors on its own

                    """Calculate any changes needed by inspecting the nodes, agents, workers, etc"""
                    """ If changes are needed, put read lock on table and make change """
                    logging.debug("Node %s", node)
                    agent = node.agent

                    logging.debug("Agent %s CPUs", agent.cpus)
                    try:
                        result = requests.get("http://" + agent.hostname + ":8002")
                        if result.status_code == 200:
                            logging.debug("Agent is alive.")
                        else:
                            raise
                    except:
                        logging.debug("Agent is down.")
                    # If there are processors pending relocation, calculate if there
                    # are free CPUs under this agent byt adding all the active processors
                    # If there are, then move the processor to this agent and node.h

                    for worker in agent.workers:
                        processor = worker.processor
                        logging.debug(
                            "Processor %s %s CPU workers",
                            processor.name,
                            processor.concurrency,
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
        import random

        import redis
        from pymongo import MongoClient

        client = MongoClient(CONFIG.get("mongodb", "uri"))
        tasks_success = 0
        with client:
            db = client.celery
            tasks_success = db.celery_taskmeta.count_documents({"status": "SUCCESS"})
            tasks_failure = db.celery_taskmeta.count_documents({"status": "FAILURE"})

        redisclient = redis.Redis.from_url(CONFIG.get("redis", "uri"))

        nodeployments = self.args

        session = get_session()
        try:
            logging.debug("DeployProcessorPlugin: Schedule run %s, %s", args, kwargs)
            logging.debug("Fetching processors to be deployed")

            # Get a random processor that either has less deployments than its concurrency needs
            processors = (
                # Read lock the processor so others cannot change it while we're looking at it
                session.query(ProcessorModel)

                #.filter(
                #    ProcessorModel.deployments.any(
                #        DeploymentModel.cpus != ProcessorModel.concurrency
                #    )
                #)
                #.with_for_update()
                .all()
                # session.query(ProcessorModel).filter(ProcessorModel.deployments.any(DeploymentModel.cpus < ProcessorModel.concurrency)).all()
                # session.query(ProcessorModel).filter(ProcessorModel.deployments.any(DeploymentModel.cpus < ProcessorModel.concurrency)).with_for_update().all()
            )
            session.commit()

            def update_stats():
                node_count = session.query(NodeModel).count()
                agent_count = session.query(AgentModel).count()
                queue_count = session.query(QueueModel).count()
                processor_count = session.query(ProcessorModel).count()
                stopped_processor_count = (
                    session.query(ProcessorModel).filter_by(status="stopped").count()
                )
                starting_processor_count = (
                    session.query(ProcessorModel)
                    .filter_by(status="stopped", requested_status="start")
                    .count()
                )
                running_processor_count = (
                    session.query(ProcessorModel).filter_by(status="running").count()
                )
                ready_processor_count = (
                    session.query(ProcessorModel).filter_by(status="ready").count()
                )
                error_processor_count = (
                    session.query(ProcessorModel).filter_by(status="error").count()
                )
                task_count = session.query(TaskModel).count()
                deployments = session.query(DeploymentModel).all()

                session.commit()
                cpu_count = 0
                cpu_running = 0

                for deployment in deployments:
                    cpu_count += deployment.cpus
                    if deployment.status == "running":
                        cpu_running += deployment.cpus

                return {
                    "nodes": node_count,
                    "agents": agent_count,
                    "queues": queue_count,
                    "processors": processor_count,
                    "processors_starting": starting_processor_count,
                    "processors_running": running_processor_count,
                    "processors_stopped": stopped_processor_count,
                    "processors_ready": ready_processor_count,
                    "processors_errored": error_processor_count,
                    "deployments": len(deployments),
                    "tasks": task_count,
                    "tasks_success": tasks_success,
                    "tasks_failure": tasks_failure,
                    "cpus_total": cpu_count,
                    "cpus_running": cpu_running,
                    "type": "stats",
                }

            stats = update_stats()
            logging.debug("Publishing stats: %s", json.dumps(stats))
            redisclient.publish("global", json.dumps(stats))

            """
            if processor is None:
                # If we didn't get any processors above, try fetching one without deployments
                processors = (
                    session.query(ProcessorModel)
                    .filter(~ProcessorModel.deployments.any())
                    .with_for_update()
                    .all()
                )
            if len(processors) == 0:
                processor = None
            else:
                processor = random.choice(processors)

            if not processor:
                processors = (
                    #session.query(ProcessorModel).with_for_update().all()
                    session.query(ProcessorModel).all()
                )
                if len(processors) == 0:
                    processor = None
                else:
                    processor = random.choice(processors)
            """

            # Try to fulfill its concurrency

            for processor in processors:
                logging.info("Checking processor %s", processor.name)
                if len(processor.deployments) == 0:
                    # I need to add deployments for this processor

                    # Look across my nodes and agents for cpus
                    # subtract running workers with concurrency to get free cpus for that node
                    # If no node can host all the cpus for the deployment, then create
                    # separate deployments with smaller cpus spread across nodes
                    pass

                scheduler = (
                    session.query(SchedulerModel).filter_by(name=self.name).first()
                )

                session.commit()
                # For this processor, determine how many deployments are needed to satisfy the concurrency parameter
                # Each node will have n free CPUs. A set of deployments are needed that map the processor concurrency needs
                # to all available CPUs across nodes.
                logging.debug("Processor concurrency is %s", processor.concurrency)

                deployed_cpus = 0

                worker_names = []

                for deployment in processor.deployments:
                    logging.debug("   Deployment: CPU %s", deployment.cpus)
                    deployed_cpus += deployment.cpus

                    if deployment.worker and deployment.worker.status == "running":
                        worker_names += [deployment.worker]

                try:
                    units = "/" + processor.ratelimit.split("/")[1]
                    rate_limit = int(processor.ratelimit.split("/")[0])
                finally:
                    rate_limit = 60
                    units = "/m"

                if len(worker_names):
                    rate_per_worker = rate_limit / len(worker_names)

                    for socket in processor.sockets:
                        """For each socket task, set the rate limit based on the processor and active workers"""
                        _taskp = socket.task.module + "." + socket.task.name
                        if processor.perworker:
                            logging.info(
                                "Setting rate limit per worker for task %s to %s",
                                _taskp,
                                processor.ratelimit + units,
                            )
                            # celery.control.rate_limit(_taskp, str(rate_per_worker)+units)
                        else:
                            logging.debug(
                                "Setting rate limit global for task %s to %s",
                                _taskp,
                                processor.ratelimit + units,
                            )
                            # celery.control.rate_limit(_taskp, processor.ratelimit+units)

                kill_workers = []

                logging.debug("No Deployments is: %s", nodeployments)
                session.commit()
                logging.info("Deployed CPUS %s, %s concurrency %s", deployed_cpus, processor.name, processor.concurrency)
                if not nodeployments and (deployed_cpus > processor.concurrency):
                    overage_cpus = deployed_cpus - processor.concurrency
                    logging.info("Concurrency overage for processor %s", processor.name)
                    logging.info("    %s:concurrency: %s", processor.name, processor.concurrency)
                    logging.info("    %s:deployments: %s", processor.name, deployed_cpus)

                    fixed_deployment = False

                    logging.info("Attempting match for overage....")
                    for deployment in processor.deployments:
                        if deployment.cpus == overage_cpus:
                            # Delete this deployment
                            kill_workers += [deployment.worker]
                            processor.deployments.remove(deployment)
                            session.commit()
                            logging.info("Deleted deployment %s with %s cpus", deployment.name, deployment.cpus)
                            fixed_deployment = True
                            break

                    if not fixed_deployment:
                        logging.info("Overage match not found. Attempting to reduce deployment CPUs....")
                        for deployment in processor.deployments:
                            if deployment.cpus > overage_cpus:
                                logging.info("Adding %s to kill_workers",deployment.worker)
                                kill_workers += [deployment.worker]
                                logging.info("Reducing CPUs for deployment %s from %s to %s", deployment.name, deployment.cpus, deployment.cpus-overage_cpus)
                                deployment.cpus -= overage_cpus
                                deployment.requested_status = 'update'
                                session.commit()
                                fixed_deployment = True

                    if not fixed_deployment:
                        """ Scan all the deployments and if their cpus are less than the overage then
                        remove that deployment and reduce the overage amount until it reaches zero or we
                        run out of deployments """
                        for deployment in processor.deployments:
                            if deployment.cpus <= overage_cpus:
                                # Delete this deployment
                                kill_workers += [deployment.worker]
                                processor.deployments.remove(deployment)
                                session.commit()
                                overage_cpus -= deployment.cpus
                                logging.info("Deleted deployment %s with %s cpus", deployment.name, deployment.cpus)

                logging.info("KILL WORKERS is %s",kill_workers)
                # TODO: Set affected workers status to 'kill' so they restart
                for worker in kill_workers:
                    logging.info("Killing worker %s",worker)
                    worker.requested_status = 'kill'
                    session.add(worker)
                    session.commit()

                if not nodeployments and (deployed_cpus < processor.concurrency):
                    logging.info("Concurrency shortfall for processor %s", processor.name)
                    logging.info("    %s:concurrency: %s", processor.name, processor.concurrency)
                    logging.info("    %s:deployments: %s", processor.name, deployed_cpus)

                    if scheduler.nodes:
                        shortfall = processor.concurrency - deployed_cpus
                        for node in scheduler.nodes:
                            agent = node.agent
                            logging.info(
                                "Agent for node %s has %s cpus",
                                node.hostname,
                                agent.cpus,
                            )

                            worker_cpus = 0
                            for worker in agent.workers:
                                logging.info(
                                    "Agent worker with %s cpus", worker.concurrency
                                )
                                if worker.deployment:
                                    worker_cpus += worker.deployment.cpus

                            occupied_cpus = 0
                            #for worker in agent.workers:
                            #    occupied_cpus += worker.deployment.cpus

                            node_deployments = session.query(DeploymentModel).filter_by(hostname=node.hostname).all()

                            for deployment in node_deployments:
                                occupied_cpus += deployment.cpus

                            logging.info(
                                "Agent %s is using %s of its %s cpus",
                                agent.name,
                                occupied_cpus,
                                agent.cpus,
                            )

                            if agent.cpus - occupied_cpus >= 1:
                                _cpus = agent.cpus - occupied_cpus
                                if _cpus > shortfall:
                                    _cpus = shortfall
                                if _cpus > 0:
                                    cpus_met = False

                                    for deployment in processor.deployments:
                                        deployment.cpus += shortfall
                                        deployment.requested_status = 'update'
                                        session.commit()
                                        break

                                    if not cpus_met:

                                        logging.info(
                                            "Creating new deployment for %s CPUS", _cpus
                                        )
                                        _deployment = DeploymentModel(
                                            cpus=_cpus,
                                            processor=processor,
                                            name=processor.name
                                            + ".deploy"
                                            + str(len(processor.deployments)),
                                            hostname=node.hostname,
                                        )
                                        processor.deployments += [_deployment]
                                        session.add(_deployment)
                                        session.add(processor)
                                        logging.info(
                                            "Deploying processor %s to node %s with %s cpus",
                                            processor.name,
                                            node,
                                            _cpus,
                                        )
                                        session.commit()
                                        redisclient.publish(
                                            "global",
                                            json.dumps(
                                                {
                                                    "processor": processor.id,
                                                    "deployment": str(_deployment),
                                                    "action": "add",
                                                }
                                            ),
                                        )
                                        shortfall -= _cpus
                                else:
                                    logging.warning("_cpus is zero")
                    else:
                        logging.info("Scheduler has no nodes.")

                if deployed_cpus == processor.concurrency:
                    logging.info("Processor %s concurrency needs are met.", processor.name)
        finally:
            session.commit()
            session.close()


class WorkPlugin(SchedulerPlugin):
    """Process work records, which are queued or scheduled tasks"""

    def run(self, *args, **kwargs):
        session = get_session()
        try:

            logging.debug("WorkPlugin: Schedule run %s %s", args, kwargs)
            logging.debug("WorkPlugin: Fetching work")
            all_work = session.query(WorkModel).all()

            for work in all_work:
                # Determine the work request and schedule or run it
                # Assign the workmodel to a worker
                logging.debug("WorkPlugin: Found work %s", work)
        finally:
            session.close()


class WatchPlugin(SchedulerPlugin):
    """Monitor reachable objects"""

    def run(self, *args, **kwargs):
        import requests

        session = get_session()
        try:

            logging.debug("WatchPlugin: Schedule run %s %s", args, kwargs)
            logging.debug("WatchPlugin: Checking nodes")
            logging.debug("WatchPlugin: Checking agents")
            agents = session.query(AgentModel).all()
            for agent in agents:
                try:
                    logging.debug(
                        "Contacting agent %s at http://%s:%s",
                        agent.name,
                        agent.hostname,
                        str(agent.port),
                    )
                    response = requests.get(
                        "http://" + agent.hostname + ":" + str(agent.port)
                    )
                    status = response.json()
                    if status["status"] == "green":
                        agent.status = "running"
                        session.add(agent)
                        session.commit()
                        session.flush()

                except Exception as ex:
                    agent.status = "down"
                    session.add(agent)
                    session.commit()
                    session.flush()
                    logging.debug("AGENT %s", agent.status)
                    logging.debug(ex)

                for worker in agent.workers:
                    logging.debug(
                        "Contacting agent worker %s at http://%s:%s",
                        worker.name,
                        worker.hostname,
                        str(worker.port),
                    )
                    try:
                        worker.status = "pending"
                        response = requests.get(
                            "http://" + worker.hostname + ":" + str(worker.port)
                        )
                        status = response.json()
                        if status["status"] == "green":
                            worker.status = "running"
                            session.add(worker)
                            session.commit()
                    except Exception as ex:
                        worker.status = "down"
                        session.add(worker)
                        session.commit()

            logging.debug("WatchPlugin: Checking workers")
            logging.debug("WatchPlugin: Checking processors")
            logging.debug("WatchPlugin: Checking plugs")

        finally:
            session.close()


_plugins = [NodePlugin, DeployProcessorPlugin, WorkPlugin, WatchPlugin]


class BasicScheduler:
    """Basic Scheduler"""

    process = None
    nodes = []

    def __init__(self, name, deployments, interval):
        self.name = name
        self.interval = interval

        self.plugins = [cls(deployments) for cls in _plugins]

        signal.signal(signal.SIGINT, self.stop)

    def stop(self, *args, **kwargs):
        [plugin.stop() for plugin in self.plugins]
        logging.info("Stopped")

    def run(self):
        [plugin.start(self.name, self.interval) for plugin in self.plugins]
        logging.info("Started")

    def start(self):
        self.process = Process(target=self.run)
        self.process.daemon = True

        return self.process
