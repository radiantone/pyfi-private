from pyfi.db import Database
from pyfi.db import Agent, Processor, Plug, Outlet
from uuid import uuid4

processor = Processor(id=uuid4(), name='proc1')
outlet = Outlet(id=uuid4(), name='outlet1')
processor.outlets += [outlet]
