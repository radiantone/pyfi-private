
"""
Class database model definitions
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
import logging

db = SQLAlchemy()


def init_db(app):
    """
    Docstring
    """
    db.init_app(app)
    app.app_context().push()

    logging.debug('Creating database model: Start')
    db.create_all()
    logging.debug('Creating database model: End')

    return db


class RoleModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'role'
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    user_id = Column(String(40), ForeignKey(
        'user.id'), nullable=False)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return '{}:{}:{}:{}'.format(self.id, self.name, self.user_id, self.lastupdated)


class UserModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'user'
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    roles = db.relationship(
        'RoleModel', backref='user', lazy=True)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return '{}:{}:{}:{}:{}'.format(self.id, self.name, self.email, self.roles, self.lastupdated)


class FlowModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'flow'
    id = Column(String(40), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    processors = db.relationship(
        'ProcessorModel', backref='flow', lazy=True)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class AgentModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'agent'
    id = Column(String(40), primary_key=True)
    name = Column(String(20), nullable=False)
    hostname = Column(String(60))
    status = Column(String(20), nullable=False)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    cpus = Column(Integer)

    def __repr__(self):
        return '{}:{}:{}:{}:{}'.format(self.id, self.cpus, self.status, self.name, self.hostname)


class ActionModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'action'
    id = Column(String(40), primary_key=True)
    name = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    params = Column(String(80))

    # host, worker, processor, queue, or all
    target = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class WorkerModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'worker'
    id = Column(String(40), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    status = Column(String(20), nullable=False)
    backend = Column(String(40), nullable=False)
    broker = Column(String(40), nullable=False)
    requested_status = Column(String(40))
    concurrency = Column(Integer)
    process = Column(Integer)
    #role = Column(String(40), nullable=False)
    #user = Column(String(40), nullable=False)
    hostname = Column(String(60))
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    processor_id = Column(String(40), ForeignKey(
        'processor.id'), nullable=True)

    def __repr__(self):
        return '{}:{}:{}:{}:{}:{}:{}'.format(self.id, self.name, self.status, self.requested_status, self.concurrency, self.process, self.hostname)


class ProcessorModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'processor'
    id = Column(String(40), unique=True, primary_key=True)
    name = Column(String(20), nullable=False)
    requested_status = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    hostname = Column(String(60))
    module = Column(String(80), nullable=False)
    gitrepo = Column(String(80))
    commit = Column(String(30))
    concurrency = Column(Integer)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    flow_id = Column(String(40), ForeignKey(
        'flow.id'), nullable=True)
    worker = db.relationship(
        'WorkerModel', backref='processor', uselist=False, lazy=True)
    queues = db.relationship('QueueModel', backref='processor', lazy=True)

    def __repr__(self):
        return '{}:{}:{}:{}:{}:{}:{}:{}'.format(self.id, self.name, self.lastupdated, self.hostname, self.concurrency, self.requested_status, self.status, self.worker)


class SettingsModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'settings'
    id = Column(String(40), primary_key=True)
    name = Column(String(20), nullable=False)
    value = Column(String(80), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class NodeModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'node'
    id = Column(String(40), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class TaskModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'task'
    id = Column(String(40), unique=True, primary_key=True)
    name = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class LogModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'log'
    id = Column(String(40), primary_key=True)
    text = Column(String(80), nullable=False)

    def __repr__(self):
        return '<id %r>' % self.id


class QueueModel(db.Model):
    """
    Docstring
    """
    __tablename__ = 'queue'
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    requested_status = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    processor_id = Column(String(40), ForeignKey('processor.id'),
                          nullable=False)

    def __repr__(self):
        return '{}:{}:{}:{}:{}'.format(self.id, self.requested_status, self.status, self.name, self.processor_id)
