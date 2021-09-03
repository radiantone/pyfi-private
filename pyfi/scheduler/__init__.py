from multiprocessing import Process, Condition
import time
import logging
from pyfi.db.model import SchedulerModel, UserModel, AgentModel, WorkerModel, PlugModel, SocketModel, ActionModel, FlowModel, ProcessorModel, NodeModel, RoleModel, QueueModel, SettingsModel, TaskModel, LogModel

import platform
HOSTNAME = platform.node()


class Scheduler:

    process = None

    def __init__(self, context, name, interval):

        self.context = context
        self.name = name
        self.interval = interval

    def run(self):

        while True:
            time.sleep(self.interval)
            logging.info("Performing schedule")

            scheduler = self.context.obj['database'].session.query(
                SchedulerModel).filter_by(name=self.name).first()

            # Perform read lock of processors without hostnames
            # Put processors in pending list to be assigned below
            # if there are available nodes, otherwise release the read lock

            for node in scheduler.nodes:
                """ Calculate any changes needed by inspecting the nodes, agents, workers, etc """
                """ If changes are needed, put read lock on table and make change """
                logging.info("Node %s", node)
                agent = node.agent
                
                logging.info("Agent %s CPUs", agent.cpus)
                # If there are processors pending relocation, calculate if there
                # are free CPUs under this agent byt adding all the active processors
                # If there are, then move the processor to this agent and node.h

                processor = agent.worker.processor
                logging.info("Processor %s %s CPU",
                                processor.name, processor.concurrency)

                # Look at all the processors for this node, if the total CPUs exceeds the nodes CPUs
                # Then determine which processor to find a better home

                # Or, for example, if you have two nodes A and B and B has 2 processors but A has none,
                # The scheduler will move one of the processors to A if A node has enough CPUs

                # Processors with 6 sockets would optimally want a node with 6 CPUs so each socket task
                # can run on its own core. This allows the scheduler to determine the compute needs for
                # each processor and locate it accordingly.
                

    def start(self):
        self.process = Process(target=self.run)
        self.process.daemon = True
        return self.process
