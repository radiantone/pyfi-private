"""
Python client API for invoking and building flows and manipulating data results
"""
import pydash as data
from pipe import select, where
from pydash import flatten, chunk, omit, get, filter_ as filter

from celery import (
    group as parallel,
    chain as pipeline,
    chord as funnel,
    chunks as segment,
)
from .objects import (
    Node,
    Processor,
    Task,
    Socket,
    Queue,
    Plug,
    Work,
    Agent,
    Argument,
    Worker,
    Network,
    Scheduler,
)
from .decorators import processor, task, node, agent, worker

__all__ = (
    "Processor",
    "Task",
    "Socket",
    "Agent",
    "Queue",
    "Plug",
    "Work",
    "Argument",
    "Node",
    "Worker",
    "Network",
    "Scheduler",
    "processor",
    "task",
    "node",
    "agent",
    "worker",
    "parallel",
    "pipeline",
    "flatten",
    "chunk",
    "omit",
    "get",
    "filter",
    "funnel",
    "segment",
    "select",
    "where",
)
