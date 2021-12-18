#!/bin/bash -x

pyfi add node -n node1 -h phoenix
pyfi add node -n node2 -h agent1 
pyfi add node -n node3 -h agent2

pyfi add agent -n agent1 -nd node1
pyfi add agent -n agent2 -nd node2
pyfi add agent -n agent3 -nd node3

pyfi add scheduler --name sched1

pyfi scheduler -n sched1  add --node node1
pyfi scheduler -n sched1  add --node node2
pyfi scheduler -n sched1  add --node node3

pyfi add processor -n proc1 -g https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor  -m pyfi.processors.sample 
pyfi add processor -n agent1proc1 -g https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor  -m pyfi.processors.sample -h agent1
pyfi add processor -n agent2proc1 -g https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor  -m pyfi.processors.sample -h agent2

pyfi add queue -n pyfi.queue1 -t direct
pyfi add queue -n pyfi.queue2 -t direct
pyfi add queue -n pyfi.queue3 -t direct

pyfi add socket -n proc1.socket1 -q pyfi.queue1 -pn proc1 -t do_something
pyfi add socket -n proc1.socket2 -q pyfi.queue1 -pn agent1proc1 -t do_this
pyfi add socket -n proc2.socket3 -q pyfi.queue1 -pn agent2proc1 -t do_that

pyfi add plug -n plug1 -q pyfi.queue2 -s proc1.socket1 -t proc1.socket2

