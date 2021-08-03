"""
agent.py - pyfi agent server responsible for managing worker/processor lifecycle on a host
"""
import platform
import logging
import multiprocessing

from sqlalchemy import inspect

from pyfi.celery.tasks import add
from pyfi.db.model import ProcessorModel, UserModel
from pyfi.blueprints.show import blueprint
from pyfi.db.model import UserModel, WorkerModel, AgentModel, QueueModel
from pyfi.worker import Worker

from flask import Flask, request, send_from_directory, current_app, send_from_directory

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(blueprint)

hostname = platform.node()
cpus = multiprocessing.cpu_count()

class Agent:

    def __init__(self, database, port, config=None, pool=4, backend='redis://192.168.1.23', broker='pyamqp://192.168.1.23'):
        self.port = port
        self.backend = backend
        self.broker = broker
        self.database = database
        self.config = config
        self.pool = pool

    def start(self, queues):
        from datetime import datetime
        import bjoern
        #from multiprocessing import Process
        from billiard.context import Process


        from uuid import uuid4

        logging.info("Serving agent on port {} {} {}".format(self.port, self.backend, self.broker))

        # Retrieve any existing Agent for this hose
        agent = self.database.session.query(
            AgentModel).filter_by(hostname=hostname).first()

        if agent is None:
            # Create database ping process to notify pyfi that I'm here and active
            # agent process will monitor database and manage worker process pool
            # agent will report local available resources to database
            # agent will report # of active processors/CPUs and free CPUs
            agent = AgentModel(id=uuid4(), hostname=hostname, name="agent")

        agent.status = 'running'
        agent.cpus = cpus
        agent.updated = datetime.now()
        self.database.session.add(agent)
        self.database.session.commit()

        def monitor_processors():
            """
            Retrieve any processors that need compute resources, determine if you have free CPU's or idle workers,
            then create a worker with the processor's module and link the worker to the processor    
            """
            import time
            
            processors = []
            workers = []

            hostname = platform.node()

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
                    logging.info("processor:monitor: sleep 3")
                    time.sleep(3)
                    logging.info("processor:monitor: wakeup %s", hostname)

                    sm = psutil.virtual_memory()
                    if sm.percent > 90.0:
                        for processor in processors:
                            if processor['worker'] is not None:
                                # Mark process last killed date and if it was killed
                                # a few times recently, then mark it stopped and save it
                                # adding a log.
                                processor['worker']['process'].kill()
                                processor['worker'] = None
                                processor['processor'].status = 'stopped'

                    if refresh == 0:
                        myprocessors = self.database.session.query(
                            ProcessorModel).filter_by(
                            hostname=hostname).all()

                    refresh += 1
                    
                    for myprocessor in myprocessors:

                        if refresh >= 100:
                            self.database.session.refresh(myprocessor)
                            refresh = 0

                        found = False
                        for processor in processors:
                            if processor['processor'].id == myprocessor.id:
                                processor['processor'] = myprocessor
                                found = True

                        if not found:
                            processors += [{'worker': None,
                                            'processor': myprocessor}]

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
                            self.database.session.delete(
                                processor['processor'].worker)
                            self.database.session.delete(
                                processor['processor'])
                            self.database.session.commit()

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

                            processor['processor'].requested_status == 'start'
                            processor['processor'].status == 'stopped'
                            processor['processor'].worker.status = 'stopped'
                            processor['processor'].worker.requested_status = 'ready'

                            logging.info("Processor is stopped")

                            self.database.session.add(
                                processor['processor'].worker)

                            self.database.session.add(
                                processor['processor'])

                            self.database.session.commit()


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

                            processor['processor'].requested_status == 'ready'
                            processor['processor'].status == 'stopped'
                            processor['processor'].worker.status = 'stopped'
                            processor['processor'].worker.requested_status = 'ready'

                            logging.info("Processor is stopped")

                            self.database.session.add(
                                processor['processor'].worker)

                            self.database.session.add(
                                processor['processor'])

                            self.database.session.commit()

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
                                process_died = not processor['worker']['wprocess'].is_alive()
                            except:
                                pass

                        logging.info("Process died: %s",process_died)
                        if (process_died or (processor['processor'].requested_status == 'update' or processor['worker'] is None)) and \
                            (processor['processor'].status != 'stopped' and processor['processor'].requested_status != 'stopped'):

                            logging.info("Updating processor")

                            if processor['processor'].worker is None:
                                """ If there is no worker model, create one and link to Processor """                                
                                workerModel = WorkerModel(id=str(uuid4()), name=processor['processor'].name+'-worker', concurrency=processor['processor'].concurrency,
                                                     status='ready',
                                                     backend=self.backend,
                                                     broker=self.broker,
                                                     hostname=hostname,
                                                     requested_status='start')

                                self.database.session.add(workerModel)
                                logging.info(
                                    "Worker %s created.", workerModel.id)
                                processor['processor'].worker = workerModel
                                self.database.session.add(processor['processor'])
                                self.database.session.commit()

                            if processor['worker'] is None or process_died:
                                """ If there is no worker Process create it """
                                import os
                                worker = {}
                            
                                dir = 'work/'+processor['processor'].id
                                os.makedirs(dir, exist_ok=True)

                                workerproc = Worker(
                                    processor['processor'], workdir=dir, pool=self.pool, database=self.database, config=self.config, backend=self.backend, broker=self.broker)

                                wprocess = workerproc.start()

                                processor['processor'].worker.requested_status = 'ready'
                                processor['processor'].worker.status = 'running'
                                self.database.session.add(
                                    processor['processor'].worker)

                                self.database.session.commit()

                                logging.info(
                                    "Worker process %s started.", workerproc.process.pid)
                                worker['worker'] = processor['processor'].worker
                                worker['worker'].process = workerproc.process.pid
                                worker['process'] = workerproc
                                processor['worker'] = worker
                                worker['wprocess'] = wprocess
                                workers += [worker]


            manage_processors(workers, processors)

        def web_server():
            try:
                bjoern.run(app, "0.0.0.0", self.port)
            except Exception as ex:
                logging.error(ex)
                logging.info("Shutting down...")

        logging.info("Monitoring processors")
        monitor_processors()


@app.route('/')
def hello():
    users = UserModel.query.all()
    _users = ""
    for user in users:
        _users += "{}:{}".format(user.username, user.email)
        _users += "\n"
    logging.debug('AgentModel API')
    result = add.delay(4, 5)
    return "Hello World from agent!! {} {}".format(result.get(), _users)
