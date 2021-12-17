"""
Python client API for invoking and building flows and manipulating data results
"""
from pipe import select, where
from celery import group as parallel, chain as pipeline, chord as funnel, chunks as segment

from pydash import flatten, flatten_deep, chunk, omit, get, find_index, filter_ as filter

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
    'find_index', 
    'flatten_deep', 
    'funnel', 
    'segment', 
    'select', 
    'where'
)
