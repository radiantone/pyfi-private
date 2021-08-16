from multiprocessing import Process, Condition
import time
import logging
from pyfi.db.model import SchedulerModel, UserModel, AgentModel, WorkerModel, PlugModel, SocketModel, ActionModel, FlowModel, ProcessorModel, NodeModel, RoleModel, QueueModel, SettingsModel, TaskModel, LogModel

import platform
HOSTNAME = platform.node()


class Scheduler:

    process = None

    def __init__(self, context):

        self.context = context

    def run(self):

        while True:
            time.sleep(3)
            logging.info("Performing schedule")

            nodes = self.context.obj['database'].session.query(
                NodeModel).filter_by(hostname=HOSTNAME).all()

            # Perform read lock of processors without hostnames
            # Put processors in pending list to be assigned below
            # if there are available nodes, otherwise release the read lock

            for node in nodes:
                logging.info("Node %s", node)

                agents = self.context.obj['database'].session.query(
                    AgentModel).filter_by(hostname=node.hostname).all()

                for agent in agents:
                    logging.info("Agent %s CPUs", agent.cpus)
                    # If there are processors pending relocation, calculate if there
                    # are free CPUs under this agent byt adding all the active processors
                    # If there are, then move the processor to this agent and node.host
                processors = self.context.obj['database'].session.query(
                    ProcessorModel).filter_by(hostname=HOSTNAME).all()

                for processor in processors:
                    logging.info("Processor %s %s CPU",
                                 processor.name, processor.concurrency)

                    # Look at all the processors for this node, if the total CPUs exceeds the nodes CPUs
                    # Then determine which processor to find a better home

    def start(self):
        self.process = Process(target=self.run)
        self.process.daemon = True
        return self.process
