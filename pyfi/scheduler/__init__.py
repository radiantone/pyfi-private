import logging
import os
import platform
import time
from multiprocessing import Process

from pyfi.db.model import SchedulerModel, WorkModel, ProcessorModel

HOSTNAME = platform.node()

if "PYFI_HOSTNAME" in os.environ:
    HOSTNAME = os.environ["PYFI_HOSTNAME"]


class Scheduler:
    """Basic Scheduler"""

    process = None

    def __init__(self, context, name, interval):

        self.context = context
        self.name = name
        self.interval = interval

    def run(self):
        import requests

        while True:
            time.sleep(self.interval)
            logging.info("Performing schedule")

            scheduler = (
                self.context.obj["database"]
                .session.query(SchedulerModel)
                .filter_by(name=self.name)
                .first()
            )

            all_work = self.context.obj["database"].session.query(WorkModel).all()

            for work in all_work:
                # Determine the work request and schedule or run it
                # Assign the workmodel to a worker
                pass
            # Perform read lock of processors without hostnames
            # Put processors in pending list to be assigned below
            # if there are available nodes, otherwise release the read lock

            processors = (
                self.context.obj["database"]
                .session.query(ProcessorModel)
                .filter_by(requested_status="deploy")
            )

            for processor in processors:
                if len(processor.deployments) == 0:
                    # I need to add deployments for this processor

                    # Look across my nodes and agents for cpus
                    # subtract running workers with concurrency to get free cpus for that node
                    # If no node can host all the cpus for the deployment, then create
                    # separate deployments with smaller cpus spread across nodes
                    pass

            # These are my nodes to manage
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

    def start(self):
        self.process = Process(target=self.run)
        self.process.daemon = True

        return self.process
