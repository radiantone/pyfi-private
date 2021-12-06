"""
Python client API for invoking and building flows
"""
from celery.utils.functional import (is_list, lookahead, maybe_list, regen,
                                     seq_concat_item, seq_concat_seq)
from celery.utils.functional import _regen
from celery.utils import abstract
from celery.utils.objects import getitem_property
from .objects import Processor, Task, Socket, Queue, Plug, Work, Agent
from celery import group as parallel, chain as pipeline, chord as funnel, chunks as segment
from celery.canvas import Signature

__all__ = ('Processor', 'Task', 'Socket', 'Agent', 'Queue', 'Plug', 'Work',
           'parallel', 'pipeline', 'funnel', 'segment')
