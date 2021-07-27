"""
agent.py - pyfi agent server responsible for managing worker/processor lifecycle on a host
"""
import socket
import logging
import multiprocessing

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

from pyfi.celery.tasks import add
from pyfi.db.model import ProcessorModel, UserModel
from pyfi.blueprints.show import blueprint
from pyfi.db.model import init_db, UserModel, WorkerModel, AgentModel, QueueModel
from pyfi.worker import Worker

from flask import Flask, request, send_from_directory, current_app, send_from_directory

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(blueprint)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

hostname = socket.gethostbyname(socket.gethostname())
cpus = multiprocessing.cpu_count()

class Agent:

    def __init__(self, database, port, backend='redis://192.168.1.23', broker='pyamqp://192.168.1.23'):
        self.port = port
        self.backend = backend
        self.broker = broker
        self.database = database

    def start(self, queues):
        from datetime import datetime
        import bjoern
        from multiprocessing import Process
        from uuid import uuid4

        logging.info("Serving agent on port {} {} {}".format(self.port, self.backend, self.broker))

        # Retrieve any existing Agent for this hose
        agent = AgentModel.query.filter_by(hostname=hostname).first()
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

        def monitor_queues():
            import time

            def manage_queues():
                from uuid import uuid4

                while True:
                    try:
                        time.sleep(3)
                        logging.info("Checking queues...")
                        queue = QueueModel.query.with_for_update(
                            of=QueueModel).filter_by(requested_status='create').first()

                        if queue is not None:
                            logging.info("Creating queue %s", queue)
                            queue.requested_status = 'ready'
                            queue.status = 'created'
                            self.database.session.commit()
                    except:
                        pass

            manage_queues()

        def monitor_processors():
            """
            Retrieve any processors that need compute resources, determine if you have free CPU's or idle workers,
            then create a worker with the processor's module and link the worker to the processor    
            """
            import time
            processors = []
            workers = []
            hostname = socket.gethostbyname(socket.gethostname())

            def manage_processors(workers, processors):
                """
                Agents manage processors assigned to them and connect them to workers
                """
                from uuid import uuid4
                import shutil
                import os

                while True:
                    logging.info("processor:monitor: sleep 3")
                    time.sleep(3)
                    logging.info("processor:monitor: wakeup %s", hostname)
                    myprocessors = ProcessorModel.query.filter_by(
                        hostname=hostname).all()

                    for myprocessor in myprocessors:
                        self.database.session.refresh(myprocessor)
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

                        if (processor['processor'].requested_status == 'update' or processor['worker'] is None) and (processor['processor'].status != 'stopped' and processor['processor'].requested_status != 'stopped'):
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

                            print(processor['processor'].worker)
                            if processor['worker'] is None:
                                """ If there is no worker Process create it """
                                import os
                                worker = {}
                            
                                dir = 'work/'+processor['processor'].id
                                os.makedirs(dir, exist_ok=True)
                                workerproc = Worker(
                                    processor['processor'], workdir=dir, backend=self.backend, broker=self.broker)
                                workerproc.start()
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

                                workers += [worker]

                            """ At this point we should have linked Processor & Worker and running worker Process """


                    processors = list(filter(lambda p: not hasattr(p,'delete'), processors))

            manage_processors(workers, processors)

        def web_server():
            try:
                bjoern.run(app, "0.0.0.0", self.port)
            except Exception as ex:
                logging.error(ex)
                logging.info("Shutting down...")

        #server = Process(target=web_server)
        #server.start()

        if queues:
            logging.info("Monitoring queues only")
            monitor_queues()
        else:
            logging.info("Monitoring processors")
            monitor_processors()

"""
Agent HTTP interface routes
"""
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
