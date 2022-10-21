"""
Python client API for invoking and building flows and manipulating data results
"""
from celery import chain as pipeline
from celery import chord as funnel
from celery import chunks as segment
from celery import group as parallel
from pipe import select, where
from pydash import chunk
from pydash import filter_ as filter
from pydash import flatten, get, omit

# from .decorators import agent, network, node, plug, processor, socket, task, worker
from .library import ProcessorBase
from .objects import (
    Agent,
    Argument,
    Deployment,
    Network,
    Node,
    Plug,
    Processor,
    Queue,
    Registry,
    Scheduler,
    Socket,
    Task,
    Work,
    Worker,
)

__all__ = (
    "Processor",
    "Task",
    "Socket",
    "Agent",
    "Queue",
    "Registry",
    "Plug",
    "Work",
    "Argument",
    "Node",
    "Deployment",
    "Worker",
    "Network",
    "Scheduler",
    "ProcessorBase",
    # "processor",
    # "task",
    # "node",
    # "agent",
    # "worker",
    # "network",
    # "socket",
    # "plug",
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
