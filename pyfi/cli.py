"""
cli.py - pyfi CLI
"""
import click
import logging


from pyfi.server import app
from pyfi.agent import app as agentapp
from pyfi.model import User, Agent, Worker, Action, Flow, Processor, Node, Queue, Settings, Task, Log, db as database
from pyfi.http import run_http


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    logging.debug(f"Debug mode is {'on' if debug else 'off'}")


@cli.group()
def proc():
    """
    Run or manage processors
    """
    pass


@cli.group()
def db():
    """
    Database operations
    """
    pass


@db.command()
def init():
    from flask import Flask

    try:
        app = Flask(__name__)

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        database.init_app(app)
        app.app_context().push()
        database.create_all()
        logging.info("Database create all schemas done.")
    except Exception as ex:
        logging.error(ex)


@proc.command()
@click.argument('function', required=True)
@click.option('--schedule', required=True)
@click.option('--queue', required=True)
def start(function, schedule, queue):
    """
    Start a processor
    """
    logging.info("Starting processor %s", function)
    # Run a worker with a beat cron schdule
    from celery import Celery
    from multiprocessing import Process

    celery = Celery('pyfi', backend='redis://localhost', broker='pyamqp://')

    @celery.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):

        # Executes every Monday morning at 7:30 a.m.
        """
        sender.add_periodic_task(
            crontab(hour=7, minute=30, day_of_week=1),
            test.s('Happy Mondays!'),
        )
        """
        # Add a wrapper task as the periodic task that retrieves
        # messages off a queue and dispatches it to the function
        pass

@cli.group()
def add():
    """
    Add an object to the database
    """
    pass


@cli.group()
def task():
    """
    Pyfi task management
    """
    pass


@task.command()
@click.argument('task', required=True)
def run(task):
    """
    Run a task
    """
    import importlib

    taskname = ''.join(task.rsplit('.')[-1])
    modulename = '.'.join(task.rsplit('.')[:-1])

    module = importlib.import_module(modulename)
    task = getattr(module, taskname)

    result = task.delay()

    print(result.get())


@add.command()
@click.argument('name')
@click.argument('email')
def user(name, email):
    """
    Add user object to the database
    """
    admin = User(username=name, email=email)
    database.session.add(admin)
    database.session.commit()
    logging.info("User %s added.", name)


@add.command()
@click.argument('name')
@click.argument('id')
def agent(name, id):
    """
    Add user object to the database
    """
    agent = Agent(name=name, id=id)
    database.session.add(agent)
    database.session.commit()
    logging.info("Agent %s added.", name)


@add.command()
@click.argument('name')
@click.argument('id')
@click.argument('worker_id')
def queue(name, id, worker_id):
    """
    Add user object to the database
    """
    worker = Worker.query.filter_by(id=worker_id).first()
    queue = Queue(name=name, id=id, worker_id=worker_id)
    worker.queues += [queue]
    database.session.add(queue)
    database.session.add(worker)
    database.session.commit()
    logging.info("Queue %s added.", name)

@cli.group()
def ls():
    """
    List database objects
    """
    pass


@cli.group()
def worker():
    """
    Run pyfi worker
    """
    pass


@worker.command()
@click.option('-h', '--host', default='worker@localhost', required=True)
@click.option('-m', '--module', required=True, multiple=True)
@click.option('-c', '--concurrency')
def start(host, module, concurrency):
    """
    Start a worker
    """
    from multiprocessing import Process
    import time
    import psutil
    import os
    import signal

    def worker_proc():
        from celery import Celery
        
        celery = Celery('pyfi', backend='redis://localhost', broker='pyamqp://', )

        worker = celery.Worker(
            include=module,
            hostname=host,
            concurrency=int(concurrency)
        )
        worker.start()

    print("Starting worker process...")
    proc = Process(target=worker_proc)
    proc.start()
    print("Started ",proc.pid)
    time.sleep(3)
    print("Suspending")
    p = psutil.Process(proc.pid)
    p.suspend()
    print("Sleeping 5")
    time.sleep(5)
    print("Awakening")
    print("Terminating")
    
    pgrp = os.getpgid(proc.pid)

    os.killpg(pgrp, signal.SIGKILL)
    proc.terminate()
    proc.kill()
    print("Terminated")


@worker.command()
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--procid', required=True)
def stop(host, procid):
    """
    Stop a worker
    """
    pass


@worker.command()
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--procid', required=True)
def status(host, procid):
    """
    Get the status of a worker
    """
    pass


@worker.command()
@click.argument('id')
@click.argument('name')
@click.argument('concurrency')
@click.argument('requested_status')
def add(id, name, concurrency, requested_status):
    """
    Add a worker request
    """
    worker = Worker(id=id, name=name, concurrency=concurrency,
                    status='ready',
                    requested_status=requested_status)
    database.session.add(worker)
    database.session.commit()
    logging.info("Worker %s added.", name)


@cli.group()
def agent():
    """
    Run pyfi agent
    """
    pass


@ls.command()
def queues():
    """
    List queues
    """
    logging.info("ls queues")


@ls.command()
def users():
    """
    List users
    """
    users = User.query.all()
    for user in users:
        print("{}:{}".format(user.username, user.email))


@ls.command()
def workers():
    """
    List users
    """
    workers = Worker.query.all()
    for _worker in workers:
        print("{}:{}:{}:{} {}".format(_worker.id, _worker.name,
              _worker.concurrency, _worker.status, _worker.queues))

@ls.command()
def agents():
    """
    List agents
    """
    agents = Agent.query.all()
    for agent in agents:
        print("{}:{}".format(agent.name, agent.id))


@cli.command()
@click.option('--port', default=8000, help='Listen port')
def api(port):
    """
    Run pyfi API server
    """
    import bjoern

    logging.info("Serving API on port {}".format(port))

    try:
        bjoern.run(app, "0.0.0.0", port)
    except Exception as ex:
        logging.error(ex)
        logging.info("Shutting down...")


@agent.command()
@click.option('--port', default=8002, help='Listen port')
@click.option('--db', default='sqlite:////tmp/test.db', help='Listen port')
def start(port, db):
    """
    Run pyfi agent server
    """
    import bjoern
    from multiprocessing import Process

    logging.info("Serving agent on port {}".format(port))
    agentapp.config['SQLALCHEMY_DATABASE_URI'] = db

    # Create database ping process to notify pyfi that I'm here and active
    # agent process will monitor database and manage worker process pool
    # agent will report local available resources to database
    # agent will report # of active processors/CPUs and free CPUs

    def monitor_workers():
        import time
        workers = []

        while True:
            logging.info("agent:monitor: sleep 3")
            time.sleep(3)
            logging.info("agent:monitor: wakeup")


            for worker in workers:
                # refresh worker from database
                database.session.refresh(worker['worker'])

                # Depending on its requested status take action
                
            # Grab a new worker request and process it
            # Only one agent will grab this worker
            _worker = Worker.query.with_for_update(of=Worker).filter_by(requested_status='deployed').first()

            if _worker is None:
                continue

            logging.info("Grabbing worker status='%s'",_worker.status)

            def worker_proc(worker, module, queues):
                from celery import Celery

                celery = Celery('pyfi', backend='redis://localhost',
                                broker='pyamqp://', )


                # Add queues to worker

                worker = celery.Worker(
                    include=module,
                    hostname=worker.name,
                    queues=['pyfi'],
                    concurrency=int(worker.concurrency)
                )
                worker.start()

                #celery.control.add_consumer('foo', reply=True,
                #                           destination=[worker.name])

            _worker.status = 'deploying'
            database.session.add(_worker)
            database.session.commit()
            process = Process(target=worker_proc,
                              args=(_worker, 'pyfi.worker', []))
            _worker.process = process.pid
            _worker.host = 'thishost'

            # Store process so it can be managed
            workers += [{'process':process, 'worker':_worker}]

            process.start()

            _worker.requested_status = 'ready'
            _worker.status = 'deployed'
            database.session.add(_worker)
            database.session.commit()

    process = Process(target=monitor_workers)
    process.start()

    try:
        bjoern.run(agentapp, "0.0.0.0", port)
    except Exception as ex:
        logging.error(ex)
        logging.info("Shutting down...")


@cli.command()
@click.option('--port', default=8001, help='Listen port')
def web(port):
    """
    Run pyfi test web server
    """
    from multiprocessing import Process

    try:
        process = Process(target=run_http, args=[port])
        process.start()
        process.join()
    except Exception as ex:
        logging.error(ex)
        logging.info("Shutting down...")
