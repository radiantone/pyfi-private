#!/bin/bash -x

flow add node -n node1 -h phoenix
flow add node -n node2 -h agent1 
flow add node -n node3 -h agent2

flow add agent -n agent1 -nd node1
flow add agent -n agent2 -nd node2
flow add agent -n agent3 -nd node3

flow add scheduler --name sched1

flow scheduler -n sched1  add --node node1
flow scheduler -n sched1  add --node node2
flow scheduler -n sched1  add --node node3

flow add processor -n proc1 -g https://github.com/radiantone/pyfi-processors#egg=ext-processor  -m ext.processors.sample
flow add processor -n agent1proc1 -g https://github.com/radiantone/pyfi-processors#egg=ext-processor  -m ext.processors.sample -h agent1
flow add processor -n agent2proc1 -g https://github.com/radiantone/pyfi-processors#egg=ext-processor  -m ext.processors.sample -h agent2

flow add queue -n pyfi.queue1 -t direct
flow add queue -n pyfi.queue2 -t direct
flow add queue -n pyfi.queue3 -t direct

flow add socket -n proc1.socket1 -q pyfi.queue1 -pn proc1 -t do_something
flow add socket -n proc1.socket2 -q pyfi.queue1 -pn agent1proc1 -t do_this
flow add socket -n proc2.socket3 -q pyfi.queue1 -pn agent2proc1 -t do_that

flow add plug -n plug1 -q pyfi.queue2 -s proc1.socket1 -t proc1.socket2

