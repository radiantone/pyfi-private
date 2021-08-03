
"""
Class database model definitions
"""
import logging

from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, Float


class RoleModel(Base):
    """
    Docstring
    """
    __tablename__ = 'role'
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return '{}:{}:{}:{}'.format(self.id, self.name, self.user_id, self.lastupdated)


user_roles = Table('user_roles', Base.metadata,
                          Column('user_id', ForeignKey('user.id')),
                          Column('role_id', ForeignKey('role.id'))
                          )

class UserModel(Base):
    """
    Docstring
    """
    __tablename__ = 'user'
    id = Column(String(40), nullable=False, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    roles = relationship("RoleModel",
                            secondary=user_roles)

    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return '{}:{}:{}:{}:{}'.format(self.id, self.name, self.email, self.roles, self.lastupdated)


class FlowModel(Base):
    """
    Docstring
    """
    __tablename__ = 'flow'
    id = Column(String(40), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    processors = relationship(
        'ProcessorModel', backref='flow', lazy=True)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class AgentModel(Base):
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


class ActionModel(Base):
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


class WorkerModel(Base):
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
    hostname = Column(String(60))
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    processor_id = Column(String(40), ForeignKey(
        'processor.id'), nullable=True)

    def __repr__(self):
        return '{}:{}:{}:{}:{}:{}:{}'.format(self.id, self.name, self.status, self.requested_status, self.concurrency, self.process, self.hostname)


class ProcessorModel(Base):
    """
    Docstring
    """
    __tablename__ = 'processor'
    id = Column(String(40), unique=True, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)
    requested_status = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    hostname = Column(String(60))
    module = Column(String(80), nullable=False)
    task = Column(String(80), nullable=False)
    gitrepo = Column(String(80))
    branch = Column(String(30))
    commit = Column(String(30))
    retries = Column(Integer)
    concurrency = Column(Integer)
    schedule = Column(Integer)
    beat = Column(Boolean)
    ratelimit = Column(String(10))
    timelimit = Column(Integer)
    ignoreresult = Column(Boolean)
    serializer = Column(String(10))
    backend = Column(String(80))
    ackslate = Column(Boolean)
    trackstarted = Column(Boolean)
    retrydelay = Column(Integer)

    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)

    flow_id = Column(String(40), ForeignKey(
        'flow.id'), nullable=True)

    worker = relationship(
        'WorkerModel', backref='processor', uselist=False, lazy=True)

    plugs = relationship('PlugModel', backref='processor', lazy=True)
    outlets = relationship('OutletModel', backref='processor', lazy=True)

    def __repr__(self):
        return '{}:{}:{}:{}:{}:{}:{}:{}:{} Plugs:{} Outlets:{}'.format(self.id, self.name, self.beat, self.lastupdated, self.hostname, self.concurrency, self.requested_status, self.status, self.worker, self.plugs, self.outlets)


class SettingsModel(Base):
    """
    Docstring
    """
    __tablename__ = 'settings'
    id = Column(String(40), primary_key=True)
    name = Column(String(20), nullable=False)
    value = Column(String(80), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class NodeModel(Base):
    """
    Docstring
    """
    __tablename__ = 'node'
    id = Column(String(40), primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    def __repr__(self):
        return '{}:{}'.format(self.id, self.name)


class TaskModel(Base):
    """
    Docstring
    """
    __tablename__ = 'task'
    id = Column(String(40), unique=True, primary_key=True)
    name = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class LogModel(Base):
    """
    Docstring
    """
    __tablename__ = 'log'
    id = Column(String(40), primary_key=True)
    text = Column(String(80), nullable=False)

    def __repr__(self):
        return '<id %r>' % self.id


outlets_queues = Table('outlets_queues', Base.metadata,
                   Column('outlet_id', ForeignKey('outlet.id')),
                   Column('queue_id', ForeignKey('queue.id'))
                   )

class OutletModel(Base):
    """
    Docstring
    """
    __tablename__ = 'outlet'
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    requested_status = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    processor_id = Column(String(40), ForeignKey('processor.id'),
                          nullable=False)
    queue = relationship(
        'QueueModel', secondary=outlets_queues, uselist=False)

    def __repr__(self):
        return '{}:{}:{}:{}:Queue:{} - Processor:{}'.format(self.id, self.requested_status, self.status, self.name, self.queue.name, self.processor_id)


plugs_queues = Table('plugs_queues', Base.metadata,
                   Column('plug_id', ForeignKey('plug.id')),
                   Column('queue_id', ForeignKey('queue.id'))
                   )

class PlugModel(Base):
    """
    Docstring
    """
    __tablename__ = 'plug'
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    requested_status = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)
    processor_id = Column(String(40), ForeignKey('processor.id'),
                          nullable=False)
    queue = relationship(
        'QueueModel', secondary=plugs_queues, uselist=False)

    def __repr__(self):
        return '{}:{}:{}:{}:Queue:{} - Processor:{}'.format(self.id, self.requested_status, self.status, self.name, self.queue.name, self.processor_id)


class QueueModel(Base):
    """
    Docstring
    """
    __tablename__ = 'queue'
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    requested_status = Column(String(20), nullable=False)
    qtype = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return '{}:{}:{}:{}:{}'.format(self.id, self.requested_status, self.status, self.name, self.lastupdated)


class QueueLogModel(Base):
    """
    Docstring
    """
    __tablename__ = 'queuelog'
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    date = Column(DateTime, default=datetime.now,
                  onupdate=datetime.now, nullable=False)
    text = Column(String(80), nullable=False)

    # processor
    # queue

    task = Column(String(80), nullable=False)
    type = Column(String(20), nullable=False)
    quantity = Column(Float)

    def __repr__(self):
        return '{}:{}:{}:{}:{}'.format(self.id, self.name, self.date, self.text)


'''
POSTGRES = 'postgresql://postgres:pyfi101@localhost:5432/pyfi'
engine = create_engine(POSTGRES, echo=True)
Base.metadata.create_all(engine)
'''
