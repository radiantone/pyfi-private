"""
Python client API for invoking and building flows and manipulating data results
"""
from pipe import select, where
from celery import group as parallel, chain as pipeline, chord as funnel, chunks as segment

from pydash import flatten, chunk, omit, get, filter_ as filter

import pydash as data

from .objects import Processor, Task, Socket, Queue, Plug, Work, Agent

__all__ = (
    'Processor', 'Task', 'Socket', 'Agent', 'Queue', 'Plug', 'Work',
    'parallel',
    'pipeline',
    'flatten',
    'chunk',
    'omit',
    'get',
    'filter',
    'funnel',
    'segment',
    'select',
    'where'
)
