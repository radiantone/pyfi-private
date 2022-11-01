#!/bin/bash -x

flow add node -n node1 -h phoenix
flow add node -n node2 -h agent1 
flow add node -n node3 -h agent2

flow add scheduler --name sched1

flow scheduler -n sched1  add --node node1
flow scheduler -n sched1  add --node phoenix.node
flow scheduler -n sched1  add --node node3

flow add processor -n proc1 -g https://github.com/radiantone/pyfi-processors#egg=ext-processor  -m ext.processors.sample
flow add processor -n agent1proc1 -g https://github.com/radiantone/pyfi-processors#egg=ext-processor  -m ext.processors.sample -h agent1
flow add processor -n agent2proc1 -g https://github.com/radiantone/pyfi-processors#egg=ext-processor  -m ext.processors.sample -h agent2

flow add queue -n pyfi.queue1 -t direct
flow add queue -n pyfi.queue2 -t direct
flow add queue -n pyfi.queue3 -t direct

flow add socket -n proc1.socket1 -q pyfi.queue1 -pn proc1 -t do_something
flow add socket -n proc1.socket2 -q pyfi.queue1 -pn proc1 -t do_this
flow add socket -n proc1a.socket1 -q pyfi.queue1 -pn agent1proc1 -t do_something
flow add socket -n proc2.socket1 -q pyfi.queue1 -pn agent2proc1 -t do_that

flow add plug -n plug1 -q pyfi.queue2 -pn proc1 -sn proc1.socket2
flow add plug -n plug3 -q pyfi.queue3 -pn proc1 
flow add plug -n plug4 -q pyfi.queue4 -pn agent1proc1 -sn proc2.socket1

#pyfi add processor -n proc2 -g https://github.com/radiantone/pyfi-processors -m ext.processors.sample  -h radiant
#pyfi add socket -n proc2.socket1 -q pyfi.queue2 -pn proc2 -t do_this 

#pyfi add processor -n proc4 -g https://github.com/radiantone/pyfi-processors -m ext.processors.sample -h radiant
#pyfi add socket -n proc4.socket1 -q pyfi.queue1 -pn proc4 -t do_something 

#pyfi add processor -n proc3 -g https://github.com/radiantone/pyfi-processors -m ext.processors.sample  -h miko
#pyfi add socket -n proc3.socket1 -q pyfi.queue3 -pn proc3 -t do_this
 

