
"""
Class database model definitions
"""
import logging

from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, Boolean, Float, literal_column, select, column


class BaseModel(Base):
    """
    Docstring
    """
    __abstract__ = True
    id = Column(String(40), primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    owner = Column(String(40), default=literal_column('current_user'))
    lastupdated = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, nullable=False)


class RoleModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'role'

    def __repr__(self):
        return '{}:{}:{}:{}'.format(self.id, self.name, self.lastupdated)


user_roles = Table('user_roles', Base.metadata,
                          Column('user_id', ForeignKey('user.id')),
                          Column('role_id', ForeignKey('role.id'))
                          )


class UserModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'user'
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(20), unique=True, nullable=False)

    roles = relationship("RoleModel",
                            secondary=user_roles)

    def __repr__(self):
        return '{}:{}:{}:{}:{}'.format(self.id, self.name, self.email, self.roles, self.lastupdated)


class FlowModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'flow'
    processors = relationship(
        'ProcessorModel', backref='flow', lazy=True)

    def __repr__(self):
        return '<Name %r>' % self.name


class AgentModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'agent'
    hostname = Column(String(60))
    status = Column(String(20), nullable=False)
    cpus = Column(Integer)
    port = Column(Integer)

    def __repr__(self):
        return '{}:{}:{}:{}:{}'.format(self.id, self.cpus, self.status, self.name, self.hostname)


class ActionModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'action'
    status = Column(String(20), nullable=False)
    params = Column(String(80))

    # host, worker, processor, queue, or all
    target = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class WorkerModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'worker'
    status = Column(String(20), nullable=False)
    backend = Column(String(40), nullable=False)
    broker = Column(String(40), nullable=False)
    requested_status = Column(String(40))
    concurrency = Column(Integer)
    process = Column(Integer)
    hostname = Column(String(60))
    processor_id = Column(String(40), ForeignKey(
        'processor.id'), nullable=True)

    def __repr__(self):
        return '{}:{}:{}:{}:{}:{}:{}'.format(self.id, self.name, self.status, self.requested_status, self.concurrency, self.process, self.hostname)


class ProcessorModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'processor'
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

    flow_id = Column(String(40), ForeignKey(
        'flow.id'), nullable=True)

    worker = relationship(
        'WorkerModel', backref='processor', uselist=False, lazy=True)

    plugs = relationship('PlugModel', backref='processor', lazy=True)
    outlets = relationship('OutletModel', backref='processor', lazy=True)

    def __repr__(self):
        return '{}:{}:{}:{}:{}:{}:{}:{}:{} Plugs:{} Outlets:{}'.format(self.id, self.name, self.beat, self.lastupdated, self.hostname, self.concurrency, self.requested_status, self.status, self.worker, self.plugs, self.outlets)


class SchedulerModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'scheduler'
    nodes = relationship('NodeModel', backref='scheduler', lazy=True)

    def __repr__(self):
        return '{}:{}:{}'.format(self.id, self.name, self.lastupdated)


class SettingsModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'settings'
    value = Column(String(80), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name


class NodeModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'node'
    hostname = Column(String(60))
    scheduler_id = Column(String(40), ForeignKey('scheduler.id'),
                          nullable=True)

    def __repr__(self):
        return '{}:{}:{}'.format(self.id, self.name, self.hostname)


class TaskModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'task'

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

class OutletModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'outlet'
    requested_status = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
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

class PlugModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'plug'
    requested_status = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    processor_id = Column(String(40), ForeignKey('processor.id'),
                          nullable=False)
    queue = relationship(
        'QueueModel', secondary=plugs_queues, uselist=False)

    def __repr__(self):
        return '{}:{}:{}:{}:Queue:{} - Processor:{}'.format(self.id, self.requested_status, self.status, self.name, self.queue.name, self.processor_id)


class QueueModel(BaseModel):
    """
    Docstring
    """
    __tablename__ = 'queue'
    requested_status = Column(String(20), nullable=False)
    qtype = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)

    def __repr__(self):
        return '{}:{}:{}:{}:{}:{}'.format(self.id, self.qtype, self.requested_status, self.status, self.name, self.lastupdated)


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

