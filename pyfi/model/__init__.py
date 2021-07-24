
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey
import logging

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    app.app_context().push()

    logging.debug('Creating database model: Start')
    db.create_all()
    logging.debug('Creating database model: End')

    return db

class User(db.Model):
    id = Column(String(40), primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Flow(db.Model):
    id = Column(String(40), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Agent(db.Model):
    id = Column(String(40), primary_key=True)
    name = Column(String(20), nullable=False)
    hostname = Column(String(60))

    def __repr__(self):
        return '{}:{}:{}'.format(self.id, self.name, self.hostname)


class Action(db.Model):
    id = Column(String(40), primary_key=True)
    name = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    params = Column(String(80))

    # host, worker, processor, queue, or all
    target = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Worker(db.Model):
    id = Column(String(40), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    status = Column(String(20), nullable=False)
    backend = Column(String(40), nullable=False)
    broker = Column(String(40), nullable=False)
    requested_status = Column(String(40))
    concurrency = Column(Integer)
    process = Column(Integer)
    hostname = Column(String(60))
    queues = db.relationship('Queue', backref='worker', lazy=True)
    processor = db.relationship('Processor', backref='processor', uselist=False, lazy=True)

    def __repr__(self):
        return '{}:{}:{}:{}:{}'.format(self.id, self.name, self.status, self.requested_status, self.concurrency, self.process, self.hostname, self.queues)


class Processor(db.Model):
    id = Column(String(40), unique=True, primary_key=True)
    name = Column(String(20), nullable=False)
    module = Column(String(80), nullable=False)
    uuid = Column(String(40), nullable=False)
    worker_id = Column(String(40), ForeignKey('worker.id'),
                        nullable=False)
                        
    def __repr__(self):
        return '{} {}'.format(self.name, self.worker_id)


class Settings(db.Model):
    id = Column(String(40), primary_key=True)
    name = Column(String(20), nullable=False)
    value = Column(String(80), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Node(db.Model):
    id = Column(String(40), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Task(db.Model):
    id = Column(String(40), unique=True, primary_key=True)
    name = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Log(db.Model):
    id = Column(String(40), primary_key=True)
    text = Column(String(80), nullable=False)

    def __repr__(self):
        return '<id %r>' % self.id


class Queue(db.Model):
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    worker_id = Column(String(40), ForeignKey('worker.id'),
                      nullable=False)

    def __repr__(self):
        return '{}:{}:{}'.format(self.id, self.name, self.worker_id)

'''
class WorkerQueues(db.Model):
    id = Column(String(40), primary_key=True)
    worker_id = Column(String(40), db.ForeignKey(
        'Worker.id'), nullable=False)
    queue_id = Column(String(40), db.ForeignKey('Queue.id'), nullable=False)
    workerR = db.relationship('Worker', foreign_keys='WorkerQueues.worker_id')
    queueR = db.relationship('Queue', foreign_keys='WorkerQueues.queue_id')

    def __repr__(self):
        return '{} {} {}'.format(self.id, self.worker_id, self.queue_id)
'''
