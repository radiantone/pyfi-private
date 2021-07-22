
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)
    app.app_context().push()

    logging.debug('Creating database model: Start')
    db.create_all()
    logging.debug('Creating database model: End')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Flow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    params = db.Column(db.String(80))

    # host, worker, processor, queue, or all
    target = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    requested_status = db.Column(db.String(40))
    concurrency = db.Column(db.Integer)
    process = db.Column(db.Integer)
    host = db.Column(db.String(60))
    queues = db.relationship('Queue', backref='worker', lazy=True)

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.id, self.name, self.status, self.requested_status, self.concurrency, self.process, self.host, self.queues)


class Processor(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    value = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Task(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<id %r>' % self.id


class Queue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'),
                      nullable=False)

    def __repr__(self):
        return '{}:{}:{}'.format(self.id, self.name, self.worker_id)

'''
class WorkerQueues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey(
        'Worker.id'), nullable=False)
    queue_id = db.Column(db.Integer, db.ForeignKey('Queue.id'), nullable=False)
    workerR = db.relationship('Worker', foreign_keys='WorkerQueues.worker_id')
    queueR = db.relationship('Queue', foreign_keys='WorkerQueues.queue_id')

    def __repr__(self):
        return '{} {} {}'.format(self.id, self.worker_id, self.queue_id)
'''
