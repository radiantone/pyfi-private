"""
agent.py - pyfi agent server responsible for managing worker/processor lifecycle on a host
"""
import socket
import logging
import asyncio

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

from pyfi.celery.tasks import add
from pyfi.model import User
from pyfi.blueprints.show import blueprint
from pyfi.model import init_db, User, Worker, Agent as PyfiAgent
from pyfi.worker import Worker as PyfiWorker

from flask import Flask, request, send_from_directory, current_app, send_from_directory

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.register_blueprint(blueprint)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

hostname = socket.gethostbyname(socket.gethostname())

class Agent:

    def __init__(self, database, port, backend='redis://192.168.1.23', broker='pyamqp://192.168.1.23'):
        self.port = port
        self.backend = backend
        self.broker = broker
        self.database = database

    def start(self):
        import bjoern
        from multiprocessing import Process
        from uuid import uuid4

        logging.info("Serving agent on port {} {} {}".format(self.port, self.backend, self.broker))

        # Create database ping process to notify pyfi that I'm here and active
        # agent process will monitor database and manage worker process pool
        # agent will report local available resources to database
        # agent will report # of active processors/CPUs and free CPUs
        agent = PyfiAgent(id=uuid4(), hostname=hostname, name="agent")
        self.database.session.add(agent)
        self.database.session.commit()

        def monitor_workers():
            import time
            workers = []
            hostname = socket.gethostbyname(socket.gethostname())
    
            while True:
                logging.info("agent:monitor: sleep 3")
                time.sleep(3)
                logging.info("agent:monitor: wakeup %s", hostname)

                myworkers = Worker.query.filter_by(hostname=hostname)
                for myworker in myworkers:
                    self.database.session.refresh(myworker)
                    found = False
                    for worker in workers:
                        logging.info("%s %s", worker['worker'].id, myworker.id)
                        print("Updating worker from ",
                            worker['worker'], " to ", myworker)
                        if worker['worker'].id == myworker.id:
                            worker['worker'] = myworker
                            found = True
                    
                    if not found:
                        workers += [{'process':None, 'worker':myworker}]

                for worker in workers:
                    try:
                        logging.info("Agent worker %s %s %s %s %s", worker['worker'].requested_status, worker['worker'].name,
                                 worker['worker'].queues, worker['worker'].backend, worker['worker'].broker)
                    except:
                        import traceback
                        print(traceback.format_exc())

                    if worker['worker'].requested_status == 'resume':
                        if worker['process'] is not None:
                            worker['process'].suspend()
                            logging.info("Suspended worker %s",
                                         worker['worker'].id)

                        worker['worker'].status = 'running'
                        worker['worker'].requested_status = 'ready'
                        self.database.session.add(worker['worker'])
                        self.database.session.commit()


                    if worker['worker'].requested_status == 'suspend':
                        if worker['process'] is not None:
                            worker['process'].suspend()
                            logging.info("Suspended worker %s",
                                         worker['worker'].id)

                        worker['worker'].status = 'suspended'
                        worker['worker'].requested_status = 'ready'
                        self.database.session.add(worker['worker'])
                        self.database.session.commit()

                    if worker['worker'].requested_status == 'start':
                        worker['worker'].status = 'ready'

                    if worker['worker'].requested_status == 'stop':
                        if worker['process'] is not None:
                            worker['process'].kill()
                            worker['process'] = None
                            logging.info("Killed worker %s",
                                            worker['worker'].id)

                        worker['worker'].status = 'stopped'
                        worker['worker'].requested_status = 'ready'
                        self.database.session.add(worker['worker'])
                        self.database.session.commit()

                    if worker['worker'].requested_status == 'kill':
                        if worker['process'] is not None:
                            worker['process'].kill()
                            worker['process'] = None
                            logging.info("Killed worker %s",
                                         worker['worker'].id)

                        worker['worker'].status = 'ready'
                        worker['worker'].requested_status = 'ready'
                        self.database.session.add(worker['worker'])
                        self.database.session.commit()

                    if (worker['worker'].requested_status == 'update' or worker['process'] is None) and worker['worker'].status != 'stopped':
                        logging.info("Updating worker")
                        if worker['process'] is not None:
                            worker['process'].kill()
                            logging.info("Killed worker %s", worker['worker'].id)
                        else:
                            logging.info("Worker process is None")

                        logging.info("Updating worker status='%s'",
                                     worker['worker'].status)

                        worker['worker'].status = 'updating'
                        self.database.session.add(worker['worker'])
                        self.database.session.commit()

                        workerproc = PyfiWorker(
                            worker['worker'], backend=self.backend, broker=self.broker)
                        workerproc.start()

                        worker['worker'].process = workerproc.process.pid

                        worker['process'] = workerproc

                        worker['worker'].process = workerproc.process.pid
                        worker['worker'].hostname = hostname
                        worker['worker'].requested_status = 'running'
                        worker['worker'].status = 'running'

                        self.database.session.add(worker['worker'])
                        self.database.session.commit()

        process = Process(target=monitor_workers)
        process.start()

        try:
            bjoern.run(app, "0.0.0.0", self.port)
        except Exception as ex:
            logging.error(ex)
            logging.info("Shutting down...")

@app.route('/')
def hello():
    users = User.query.all()
    _users = ""
    for user in users:
        _users += "{}:{}".format(user.username, user.email)
        _users += "\n"
    logging.debug('Agent API')
    result = add.delay(4, 5)
    return "Hello World from agent!! {} {}".format(result.get(), _users)
