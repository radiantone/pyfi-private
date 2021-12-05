"""
agent.py - pyfi agent server responsible for managing worker/processor lifecycle on a host
"""
import platform
import logging
import multiprocessing
import configparser
import os
import psutil
import shutil
import glob
import signal

from contextlib import contextmanager

from pathlib import Path

from sqlalchemy import inspect

from pyfi.db.model import ProcessorModel, UserModel
from pyfi.blueprints.show import blueprint
from pyfi.db.model import UserModel, WorkerModel, AgentModel, QueueModel, NodeModel
from pyfi.worker import Worker

from flask import Flask, request, send_from_directory, current_app, send_from_directory

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

app.register_blueprint(blueprint)

home = str(Path.home())

CONFIG = configparser.ConfigParser()

hostname = platform.node()

cpus = multiprocessing.cpu_count()


@app.route("/kill")
def kill():
    from psutil import Process


    with open('agent.pid','r') as procfile:
        pid = int(str(procfile.read()).strip())
        logging.info("Shutting down...%s", pid)
        process = psutil.Process(pid)

        '''
        logging.info("Killing sub processes....")
        for child in process.children(recursive=True):
            logging.info("Killing child....")
            child.kill()
            logging.info("Killed child....")
        '''
        
        logging.info("Killing agent....")
        process.kill()
        logging.info("Terminating agent....")
        process.terminate()

        logging.info("Killing web process....")
        process = psutil.Process(os.getpid())
        process.kill()
        process.terminate()

    return "Shutdown complete"


class Agent:
    """ Agent class """

    @contextmanager
    def get_session(self):
        session = self.database.session

        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()

    def __init__(self, database, dburi, port, config=None, clean=False, user=None, pool=4, backend='redis://localhost', broker='pyamqp://localhost', size=10):
        self.port = port
        self.backend = backend
        self.broker = broker
        self.database = database
        self.config = config
        self.pool = pool
        self.dburi = dburi
        self.node = None
        self.agent = None
        self.user = user
        self.size = size

        if clean:
            logging.info("Cleaning work directories")
            if os.path.exists("work"):
                workdirs = glob.glob("work/*")

                for workdir in workdirs:
                    logging.info("Removing workdir %s", workdir)
                    shutil.rmtree(workdir)
                
        logging.info("Checking config at %s", home+"/pyfi.ini")
        if os.path.exists(home+"/pyfi.ini"):
            CONFIG.read(home+"/pyfi.ini")
            self.backend = CONFIG.get('backend', 'uri')
            self.broker = CONFIG.get('broker', 'uri')

    def start(self):
        from datetime import datetime
        import bjoern
        from billiard.context import Process
        from uuid import uuid4


        with open('agent.pid','w') as procfile:
            procfile.write(str(os.getpid()))

        logging.info("Serving agent on port {} {} {}".format(
            self.port, self.backend, self.broker))

        # Retrieve any existing Agent for this hose
        agent = self.database.session.query(
            AgentModel).filter_by(hostname=hostname).first()

        if agent is None:
            # Create database ping process to notify pyfi that I'm here and active
            # agent process will monitor database and manage worker process pool
            # agent will report local available resources to database
            # agent will report # of active processors/CPUs and free CPUs
            agent = AgentModel(hostname=hostname,
                               name=hostname+".agent")

        agent.status = "starting"
        self.agent = agent
        vmem = psutil.virtual_memory()

        node = self.database.session.query(NodeModel).filter_by(hostname=hostname).first()
        
        if node is None:
            node = NodeModel(name=hostname+".node", agent=self.agent, hostname=hostname)
            with self.get_session() as session:
                session.add(node)
            
            self.database.session.refresh(node)
        else:
            self.database.session.add(node)

        if node.agent is None:
            node.agent = agent

        agent.node_id = node.id

        node.cpus = cpus
        node.memsize = vmem.total
        node.freemem = vmem.free
        node.memused = vmem.percent
        self.node = node

        agent.status = 'running'
        agent.cpus = cpus
        agent.port = self.port
        agent.updated = datetime.now()

        with self.get_session() as session:
            session.add(agent)

        def monitor_processors():
            """
            Retrieve any processors that need compute resources, determine if you have free CPU's or idle workers,
            then create a worker with the processor's module and link the worker to the processor    
            """
            import time

            processors = []
            workers = []

            def manage_processors(workers, processors):
                """
                Agents manage processors assigned to them and connect them to workers
                """
                from uuid import uuid4
                import psutil
                import shutil
                import os
                refresh = 0

                while True:
                    vmem = psutil.virtual_memory()

                    self.node.memsize = vmem.total
                    self.node.freemem = vmem.free
                    self.node.memused = vmem.percent

                    with self.get_session() as session:
                        session.add(self.node)

                    time.sleep(3)
                    sm = psutil.virtual_memory()
                    if sm.percent > 90.0:
                        # Send health alert log
                        for processor in processors:
                            if processor['worker'] is not None:
                                # Mark process last killed date and if it was killed
                                # a few times recently, then mark it stopped and save it
                                # adding a log.
                                processor['worker']['process'].kill()
                                processor['worker'] = None
                                processor['processor'].status = 'stopped'

                    myprocessors = []

                    # Gather host information and update node

                    if refresh == 0:
                        # Time to refresh all the processors from the database
                        myprocessors = self.database.session.query(
                            ProcessorModel).filter_by(
                            hostname=hostname).all()

                        # Loop through existing processor references and refresh from database
                        # Check for moved processors
                        for processor in processors:
                            self.database.session.refresh(
                                processor['processor'])

                            if processor['processor'].hostname != hostname:
                                # Processor of mine has been moved, kill it
                                if processor['worker'] is not None:

                                    processor['processor'].requested_status = 'move'

                                    with self.get_session() as session:
                                        session.add(processor['processor'])
                                    #self.database.session.add(processor['processor'])
                                    

                                    logging.info("Processor {} moved from {} to {}.".format(
                                        processor['processor'].name, hostname, processor['processor'].hostname))
                                    logging.info("Killing processor {}.".format(
                                        processor['processor'].name))
                                    processor['worker']['process'].kill()
                                    processor['worker'] = None
                                    processors.remove(processor)
                                    logging.info("Removed processor {} from list.".format(
                                        processor['processor'].name))

                                    processor['processor'].requested_status = 'update'

                                    with self.get_session() as session:
                                        session.add(processor['processor'])
                                    

                        # Loop through my database processors
                        for myprocessor in myprocessors:

                            self.database.session.refresh(myprocessor) # Might not be needed
                            if myprocessor.requested_status == 'move':
                                continue

                            found = False
                            for processor in processors:
                                if processor['processor'].id == myprocessor.id:
                                    # If I already have it in my cache, update it
                                    processor['processor'] = myprocessor
                                    found = True

                            if not found:
                                # If this is a new processor, add it to cache
                                processors += [{'worker': None,
                                                'processor': myprocessor}]

                    refresh += 1
                    if refresh >= 3: # 3 cycle interval
                        refresh = 0

                    # Loop through my processor cache again and operate on them based
                    # on requested_status
                    for processor in processors:

                        if processor['processor'].requested_status == 'removed':
                            if processor['worker'] is not None:
                                logging.info("Killing worker")
                                try:
                                    processor['worker']['process'].kill()
                                    processor['worker'] = None
                                    logging.info("Killed worker %s",
                                                 worker['worker'].id)
                                except:
                                    import traceback
                                    print(traceback.format_exc())

                            processor['delete'] = True

                            with self.get_session() as session:
                                session.delete(processor['processor'].worker)
                                session.delete(processor['processor'])
                            

                            if os.path.exists('work/'+processor['processor'].id):
                                logging.debug(
                                    "Removing work directory %s", 'work/'+processor['processor'])
                                shutil.rmtree('work/'+processor['processor'])

                            logging.info("Processor is removed")

                            continue

                        if processor['processor'].requested_status == 'restart':
                            if processor['worker'] is not None:
                                logging.info("Killing worker")
                                try:
                                    processor['worker']['process'].kill()
                                    processor['worker'] = None
                                    logging.info("Killed worker %s",
                                                 worker['worker'].id)
                                except:
                                    import traceback
                                    print(traceback.format_exc())

                            processor['processor'].requested_status = 'start'
                            processor['processor'].status = 'stopped'
                            processor['processor'].worker.status = 'stopped'
                            processor['processor'].worker.requested_status = 'ready'

                            logging.info("Processor is stopped")

                            with self.get_session() as session:
                                session.add(processor['processor'].worker)
                                session.add(processor['processor'])

                        if processor['processor'].requested_status == 'paused':
                            if processor['worker'] is not None:
                                logging.info("Pausing worker")
                                try:
                                    processor['worker']['process'].suspend()
                                    logging.info("Paused worker %s",
                                                 worker['worker'].id)
                                except:
                                    import traceback
                                    print(traceback.format_exc())

                            processor['processor'].requested_status = 'ready'
                            processor['processor'].status = 'paused'
                            processor['processor'].worker.status = 'paused'
                            processor['processor'].worker.requested_status = 'ready'

                            logging.info("Processor is paused")

                            with self.get_session() as session:
                                session.add(processor['processor'].worker)
                                session.add(processor['processor'])
                            #self.database.session.add(
                            #    processor['processor'].worker)

                            #self.database.session.add(
                            #    processor['processor'])

                            
                            continue

                        if processor['processor'].requested_status == 'resumed':
                            if processor['worker'] is not None:
                                logging.info("Resuming worker")
                                try:
                                    processor['worker']['process'].resume()
                                    logging.info("Paused worker %s",
                                                 worker['worker'].id)
                                except:
                                    import traceback
                                    print(traceback.format_exc())

                            processor['processor'].requested_status = 'ready'
                            processor['processor'].status = 'resumed'
                            processor['processor'].worker.status = 'resumed'
                            processor['processor'].worker.requested_status = 'ready'

                            logging.info("Processor is resumed")

                            with self.get_session() as session:
                                session.add(processor['processor'].worker)
                                session.add(processor['processor'])

                            
                            continue

                        if processor['processor'].requested_status == 'stopped':
                            if processor['worker'] is not None:
                                logging.info("Killing worker")
                                try:
                                    processor['worker']['process'].kill()
                                    processor['worker'] = None
                                    logging.info("Killed worker %s",
                                                 worker['worker'].id)
                                except:
                                    import traceback
                                    print(traceback.format_exc())

                            processor['processor'].requested_status = 'ready'
                            processor['processor'].status = 'stopped'
                            processor['processor'].worker.status = 'stopped'
                            processor['processor'].worker.requested_status = 'ready'

                            logging.info("Processor is stopped")

                            with self.get_session() as session:
                                session.add(processor['processor'].worker)
                                session.add(processor['processor'])

                        if processor['processor'].requested_status == 'started':
                            if processor['worker'] is None:
                                # Spin up worker if I have CPU's available
                                # Create a worker, link it to the processor
                                # Add it to workers list
                                pass
                            pass

                        """
                        If the worker python Process is no longer alive, restart it as long as the processor is not in stopped state.
                        Otherwise, if processor requested state is 'update', then restart process
                        or if processor worker is None, restart it (e.g. on startup)
                        """
                        process_died = False
                        if 'worker' in processor:
                            try:
                                process_died = not processor['worker']['wprocess'].is_alive(
                                )
                            except:
                                pass

                        if (processor['processor'].requested_status == 'start' or (process_died or (processor['processor'].requested_status == 'update' or processor['worker'] is None)) and
                                (processor['processor'].status != 'stopped' and processor['processor'].requested_status != 'stopped')):

                            logging.info("Updating processor")

                            if processor['worker'] is not None:
                                processor['worker']['process'].kill()
                                processor['worker'] = None

                            '''
                            TODO: Separate out the worker process into `pyfi worker start --name <name>` so it can be run in its own virtualenv as a child process here
                            This will allow the gitrepo to be installed in the virtualenv for that processor and kept separate from this agent environment
                            Once a WorkerModel has been created with all the details, spawn `pyfi worker start` FROM the virtualenv after the gitrepo setup.py has been
                            installed.
                            '''
                            if processor['processor'].worker is None:
                                """ If there is no worker model, create one and link to Processor """

                                # TODO: Not sure this is needed since worker now puts worker model row in database
                                workerModel = self.database.session.query(
                                    WorkerModel).filter_by(name=hostname+".agent."+processor['processor'].name+'.worker').first()

                                if workerModel is None:
                                    logging.info("Creating worker model...")
                                    workerModel = WorkerModel(id=str(uuid4()), name=hostname+".agent."+processor['processor'].name+'.worker', concurrency=processor['processor'].concurrency,
                                                          status='ready',
                                                          backend=self.backend,
                                                          broker=self.broker,
                                                          agent_id=self.agent.id,
                                                          hostname=hostname,
                                                          requested_status='start')

                                workerModel.lastupdated = datetime.now()
                                workerModel.status = 'running'
                                workerModel.processor = processor['processor']

                                with self.get_session() as session:
                                    session.add(self.agent)
                                    session.add(workerModel)
                                    logging.info("Worker model is %s", workerModel)
                                    logging.info("Agent worker is %s",
                                                self.agent.worker)
                                    self.agent.worker = workerModel
                                
                                logging.info(
                                    "Worker %s created.", workerModel.id)

                                processor['processor'].worker = workerModel

                            if processor['worker'] is None or process_died:
                                # If there is no worker Process create it
                                worker = {}

                                dir = 'work/'+processor['processor'].id
                                os.makedirs(dir, exist_ok=True)
                                logging.info("Agent: Creating Worker() queue size %s", self.size)
                                workerproc = Worker(
                                    processor['processor'], size=self.size, workdir=dir, user=self.user, pool=self.pool, database=self.dburi, celeryconfig=self.config, backend=self.backend, broker=self.broker)

                                # Setup the virtualenv only

                                workerproc.start(start=False)

                                # Launch from the virtualenv
                                wprocess = workerproc.launch(processor['processor'].worker.name, self.pool)
                                #wprocess = workerproc.start()

                                processor['processor'].worker.requested_status = 'ready'
                                processor['processor'].worker.status = 'running'

                                with self.get_session() as session:
                                    session.add(processor['processor'].worker)

                                logging.info(
                                    "Worker process %s started.", wprocess.pid)

                                worker['worker'] = processor['processor'].worker
                                worker['worker'].process = workerproc.process.pid
                                worker['process'] = workerproc
                                worker['wprocess'] = wprocess

                                processor['worker'] = worker

                                workers += [worker]

                            processor['processor'].requested_status = 'ready'
                            processor['processor'].status = 'running'

                            with self.get_session() as session:
                                session.add(processor['processor'])

            manage_processors(workers, processors)

        def web_server():
            from setproctitle import setproctitle

            try:
                setproctitle('pyfi agent::web_server')
                logging.info("Starting web server on %s",self.port)
                bjoern.run(app, "0.0.0.0", self.port)
            except Exception as ex:
                logging.error(ex)
                logging.info("Shutting down...")

        webserver = Process(target=web_server, daemon=True)
        webserver.start()

        logging.info("Monitoring processors")
        monitor_processors()


@app.route('/')
def hello():
    return "Agent is running"
